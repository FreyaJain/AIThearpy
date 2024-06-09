import torch
from torch import nn
from api.models import *
from api.models.pytorch import *


class AITherapy(nn.Module):
    def __init__(self, vocab_size, embedding_size, hidden_size, output_size, num_layers
               , bidirectional, dropout, pad_idx):
        super(AITherapy, self).__init__()

        self.embedding = nn.Sequential(
            nn.Embedding(vocab_size, embedding_dim=embedding_size, padding_idx=pad_idx),
            nn.Dropout(dropout)
        )
        self.lstm = nn.Sequential(
            nn.LSTM(
            embedding_size, 
            hidden_size=hidden_size, 
            bidirectional=bidirectional, 
            num_layers=num_layers,
            dropout=dropout
            )
        )
        self.out = nn.Sequential(
            nn.Linear(hidden_size * 2, out_features=128),
            nn.Dropout(dropout),
            nn.Linear(128, out_features=output_size),
            nn.Dropout(dropout)
        )

    def forward(self, text, text_lengths):
        embedded = self.embedding(text)
        packed_embedded = nn.utils.rnn.pack_padded_sequence(embedded, text_lengths.to('cpu'), enforce_sorted=False, batch_first=True)
        packed_output, (h_0, c_0) = self.lstm(packed_embedded)
        output, output_lengths = nn.utils.rnn.pad_packed_sequence(packed_output)
        output = torch.cat((h_0[-2,:,:], h_0[-1,:,:]), dim = 1)
        return self.out(output)
     
print(" ✅ LOADING PYTORCH AI Therapy MODEL!\n") 
INPUT_DIM = len(stoi) 
EMBEDDING_DIM = 100
HIDDEN_DIM = 256
OUTPUT_DIM = len(labels_dict)
N_LAYERS = 2
BIDIRECTIONAL = True
DROPOUT = 0.5
PAD_IDX = stoi[PAD_TOKEN] 
ai_therapy_model = AITherapy(
              INPUT_DIM, 
              EMBEDDING_DIM, 
              HIDDEN_DIM, 
              OUTPUT_DIM, 
              N_LAYERS, 
              BIDIRECTIONAL, 
              DROPOUT, 
              PAD_IDX
).to(device)
     
ai_therapy_model.load_state_dict(torch.load(PYTORCH_THERAPY_MODEL_PATH, 
                                     map_location=device))
print(" ✅ LOADING PYTORCH AI Therapy MODEL DONE!\n")


