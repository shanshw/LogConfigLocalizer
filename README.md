# Introduction
The repository shows the source code of LogConfigLocalizer proposed in the paper [**Face It Yourselves: An LLM-based Two-stage Strategy to Localize Configuration Errors via Logs**](https://arxiv.org/pdf/2404.00640).

![Overview](fig/overview.png)

-----------
# Parser
To make use of it, please refer to [README](https://github.com/shanshw/LogConfigLocalizer/blob/main/src/parser/README.md) in src/parser.

# Localizer
To make use of it, please refer to [README](https://github.com/shanshw/LogConfigLocalizer/blob/main/src/localizer/README.md) in src/localizer.

# Reproduction
For the experimental results, please refer to the [benchmark](benchmark/README.md). 

To reproduce the results in the paper, please refer to [README](https://github.com/shanshw/LogConfigLocalizer/blob/main/src/scripts/README.md) in src/scripts.


# Citation
If the released code is useful for your research, please cite the following paper:
```
@inproceedings{shan2024face,
  title={Face it yourselves: An llm-based two-stage strategy to localize configuration errors via logs},
  author={Shan, Shiwen and Huo, Yintong and Su, Yuxin and Li, Yichen and Li, Dan and Zheng, Zibin},
  booktitle={Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis},
  pages={13--25},
  year={2024}
}
```
