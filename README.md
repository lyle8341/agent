

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



+ 取消代理
  + conda config --remove proxy_servers.http
  + conda config --remove proxy_servers.https