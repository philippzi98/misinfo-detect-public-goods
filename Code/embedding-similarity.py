# =============================================================================
# Section 1: Setup
# =============================================================================

# Import libraries (and ensure Python 3.10.6)
import torch # Ensure torch 2.1.0
import time
import os
import numpy as np
import pandas as pd
from glob import glob
from sentence_transformers import SentenceTransformer # Ensure sentence_transformers 2.2.2
from pyarrow.parquet import ParquetFile
from multiprocessing import Pool, shared_memory
from numba import jit

# Set up environment variables
def get_env_var(varname, default):
    if os.environ.get(varname) != None:
        var = int(os.environ.get(varname))
        print(varname, ':', var)
    else:
        var = default
        print(varname, ':', var, '(Default)')
    return var

# Fetching environment variables set by SLURM
SLURM_JOB_ID = get_env_var('SLURM_JOB_ID', 0)
SLURM_ARRAY_TASK_ID = get_env_var('SLURM_ARRAY_TASK_ID', 0)
SLURM_ARRAY_TASK_COUNT = get_env_var('SLURM_ARRAY_TASK_COUNT', 1)
SLURM_CPUS_PER_TASK = get_env_var('SLURM_CPUS_PER_TASK', 2)

# Constants
start_time = time.time()
MODEL_PATH = './models/gte-large-finetuned-11162023.pth' # Add your path
CLAIMS_EMBDS_PATH = './data/claims/claims_embeddings_11282023.pkl' # Add your path
TWEETS_PATH = './data/tweets/' # Add your path
OUTPUT_PATH = '.data/output/' # Add your path

#BATCH_SIZE = 100 # Uncomment if you want to batch
#NUM_WORKERS = SLURM_CPUS_PER_TASK # Uncomment if you want to parallelize

# =============================================================================
# Section 2: Load model and claim embeddings 
# =============================================================================

# Load model
model = SentenceTransformer('thenlper/gte-large') 
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cuda' if torch.cuda.is_available() else 'cpu')))
model.to(torch.device('cuda' if torch.cuda.is_available() else 'cpu')) # Move model to GPU if available
model.eval()

# Load and share claim embeddings
claims_df = pd.read_parquet(CLAIMS_EMBDS_PATH)

# Define structured array dtype based on your embeddings length
embedding_length = len(claims_df['embeddings'].iloc[0])
dtype = [('claim_id', 'int64'), ('verdict', 'int64'), ('embeddings', 'float32', (embedding_length,))]

# Create structured array
structured_array = np.zeros(len(claims_df), dtype=dtype)
structured_array['claim_id'] = claims_df['claim_id'].to_numpy()
structured_array['verdict'] = claims_df['verdict'].to_numpy()
for i, emb in enumerate(claims_df['embeddings']):
    structured_array['embeddings'][i] = emb


# =============================================================================
# Section 3: Define functions
# =============================================================================

# Adapted pairwise distance computation function using Numba for batch processing
@jit(nopython=True)
def compute_similarity_batch(tweet_embeddings, claims_embeddings):
    # Assuming claims_embeddings and tweet_embeddings are numpy arrays
    if claims_embeddings.shape[1] != tweet_embeddings.shape[1]:
        raise ValueError("Dimensionality of claim embeddings and tweet embeddings do not match.")
    similarities = np.zeros((tweet_embeddings.shape[0], claims_embeddings.shape[0]), dtype=np.float32)
    for t_index, tweet_embedding in enumerate(tweet_embeddings):
        for c_index, claim_embedding in enumerate(claims_embeddings):
            norm_tweet = np.linalg.norm(tweet_embedding)
            norm_claim = np.linalg.norm(claim_embedding)
            # Check to prevent division by zero
            if norm_tweet > 0 and norm_claim > 0:
                similarity = np.dot(tweet_embedding, claim_embedding) / (norm_tweet * norm_claim)
            else:
                similarity = 0.0 
            similarities[t_index, c_index] = similarity
    return similarities


# =============================================================================
# Section 4: Similarity computation with job array functionality
# =============================================================================

# Fetch a list of all tweets files (in case tweets data is stored across multiple files)
all_files = glob(os.path.join(TWEETS_PATH, '*.parquet'))
pf = ParquetFile(all_files[SLURM_ARRAY_TASK_ID])
pf = pf.read()
data = pf.to_pandas()
batch_size = 1 # We ran this script across a large number of job arrays with little memory; adapt if you choose different settings
num_batches = int(len(data) / batch_size )

# Actual similarity computation
output_file_path = os.path.join(OUTPUT_PATH, f"batch_{SLURM_ARRAY_TASK_ID}.txt")
if not os.path.exists(output_file_path):
    with open(output_file_path, 'w') as file:
        file.write('claim_id,verdict,tweet_id,similarity_score\n')
for i in range(num_batches):
    print(i)
    start_idx = i * batch_size
    end_idx = (i + 1) * batch_size
    batch_data = data.iloc[start_idx:end_idx]
    tweet_embeddings = model.encode(batch_data['tweet_text'].tolist())
    tweet_embeddings = np.ascontiguousarray(np.array(tweet_embeddings).astype(np.float32))
    claims_embeddings = np.ascontiguousarray(structured_array['embeddings'].astype(np.float32))
    similarity_scores = compute_similarity_batch(tweet_embeddings, claims_embeddings)
    output_data = []
    for t_index, tweet_id in enumerate(batch_data['tweet_id']):
        for c_index in range(len(structured_array)):
            claim_id = structured_array['claim_id'][c_index]
            verdict = structured_array['verdict'][c_index]
            similarity_score = similarity_scores[t_index, c_index]
            if similarity_score > 0.9: # We chose 0.9 as initial cut-off threshold; adapt if you want to take a different approach
                print("now")
                output_data.append((claim_id, verdict, tweet_id, similarity_score))
    if output_data:
        with open(output_file_path, 'a') as file:
            for row in output_data:
                file.write(','.join(map(str, row)) + '\n')

# Finish job and print duration
end_time = time.time()
duration = end_time - start_time
hours = duration/3600
print(f"The job completed successfully in {hours} hours.")
