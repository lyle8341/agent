# agent开发

### 如何下载安装包
+ 使用pip
  ```shell
  #安装包（默认是最新版）
  pip install langchain
  #指定版本
  pip install langchain=0.3.7
  #批量安装
  pip install langchain requests numpy
  #升级包
  pip install --upgrade langchain
  #卸载包
  pip uninstall langchain
  #查看已安装包
  pip list
  #镜像加速
  pip install -i https://mirrors.aliyun.com/pypi/simple langchain
  #从本地安装
  pip install ./local_package.whl
  pip install https://github.com/user/repo/archive/main.zip
  ```
+ 使用conda
  ```shell
  #安装包（默认仓库）
  conda install langchain
  #指定频道（如 conda-forge)
  conda install -c conda-forge langchain=0.3.7
  #更新包
  conda update langchain
  #卸载包
  conda uninstall langchain
  #查看已安装包
  conda list
  ```
  > -c: 是--channel都缩写  
  > 二者最好不要混用，推荐先用conda，后pip补充
  




+ jupyter如果需要使用uv安装的包的话
  + uv run --with jupyter jupyter lab


+ https://huggingface.co/


+ 使用 Git LFS（Large File Storage）
  + 安装 Git LFS
    > git lfs install
  + 追踪文件类型（比如 .bin, .tar 等大文件）
    > git lfs track "*.bin"
  + 提交大文件
    ```shell
    git add .gitattributes
    git add large_file.bin
    git commit -m "Add large file"
    git push
    ```

+ 1.设置 Git 的压缩线程
  > git config --global pack.threads 8
+ 2.设置 Git 的内存限制
  + 配置 Git 的缓存大小
    ```shell
    git config --global core.preloadIndex true
    git config --global core.fscache true
    ```
  + 配置 Git 的压缩内存限制
    ```shell
    git config --global pack.windowMemory 100m
    ```
+ 3.调节 Git 的压缩级别
  > git config --global core.compression 9
+ 4.增加 Git 的 HTTP 传输缓冲区
  > git config --global http.postBuffer 524288000
+ 这会让 git clone 只获取最新的提交历史，减少不必要的数据下载
  > git config --global clone.depth 1



# conda环境迁移
+ 1.MacOS上导出当前环境配置
  > conda env export > environment.yml
+ 2.迁移到Windows上
  > conda env create -f environment.yml
+ 3.修复调整差异导致的问题

+ 配置代理
  + .condarc文件
  + proxies: 注意是proxies

+ torch，numpy版本问题
  ```pycon
  conda install pytorch torchvision torchaudio -c pytorch
  ```

+ PyTorch 在 Mac MPS（Metal Performance Shaders）后端的显存不足错误
  ```shell
  #方式一
  export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0
  #方式二 
  import os
  os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"
  注意：要写在 import torch 之前。
  ```




### LangChain
```
LangChain是一个帮助你构建LLM应用到 全套工具集。涉及prompt构建、LLM接入、记忆管理、工具调用、Rag、智能体开发等
```






+ [视频地址](https://www.bilibili.com/video/BV1ZppNzHEY4?spm_id_from=333.788.player.switch&vd_source=26a4c9cd3b93c3c6110a2ce9403ca5ea&p=3)