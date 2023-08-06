<img src="./diagram.png" width="700px"></img>

## Lie Transformer - Pytorch (wip)

Implementation of <a href="https://arxiv.org/abs/2012.10885">Lie Transformer</a>, Equivariant Self-Attention, in Pytorch. Only the SE3 version will be present in this repository, as it may be needed for Alphafold2 replication.

## Install

```bash
$ pip install lie-transformer-pytorch
```

## Usage

```python
import torch
from lie_transformer_pytorch import LieTransformer

model = LieTransformer(
	dim = 512,
	num_layers = 1
)

x = torch.randn(1, 64, 512)
coors = torch.randn(1, 64, 3)
mask = torch.ones(1, 64).bool()

out = model((coors, x, mask)) # (1, 1)
```

## Citations

```bibtex
@misc{hutchinson2020lietransformer,
    title={LieTransformer: Equivariant self-attention for Lie Groups}, 
    author={Michael Hutchinson and Charline Le Lan and Sheheryar Zaidi and Emilien Dupont and Yee Whye Teh and Hyunjik Kim},
    year={2020},
    eprint={2012.10885},
    archivePrefix={arXiv},
    primaryClass={cs.LG}
}
```
