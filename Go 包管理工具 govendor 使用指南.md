# Go 包管理工具 govendor 使用指南

govendor 是 go 语言依赖管理工具。

## 安装及初始化
安装：
```
go get -u -v github.com/kardianos/govendor
```
初始化：
```
# Setup your project.
cd "my project in GOPATH"
govendor init

# Add existing GOPATH files to vendor.
govendor add +external
```

## 下载依赖包
下面介绍三个命令：

- `govendor fetch`：不但可以下载自身的包，还可以下载依赖。
- `govendor get`：如官网所述 Like "go get" but copies dependencies into a "vendor" folder，实际上只复制了依赖包进到 vendor 目录而已。
- `govendor add`：Add packages from $GOPATH，意思是从本地加载依赖包。

综上，如果是下载依赖包，一定是用 `govendor fetch`。

```
govendor fetch github.com/gin-gonic/gin@v1.2 # 只拷贝 gin/ 目录的内容，而不包含其子目录
govendor fetch github.com/gin-gonic/gin/...@v1.2 # 可以得到 gin/ 目录，及其所有子目录
```
`@v1.2` 表示使用 v1.2 版本，其实就是 git tag 为 v1.2 的 revision，这个功能很实用。

再说一个可能会碰到的问题，有时候我们使用第三方依赖包，而且还有 bug，修复之后，期望使用自己仓库的时候，可以这样做：

```
govendor get 'github.com/go-sql-driver/mysql::github.com/yongxinz/go-mysql'
```
原仓库的 `github.com/go-sql-driver/mysql` 存在一个小问题，此时期望使用自己修复过的 `github.com/yongxinz/go-mysql`。

## 版本管理
不要将整个 `vendor/` 目录的内容都提到 git 仓库，只提交 `vendor/vendor.json` 文件就可以了。

当我们拉代码之后，需要安装依赖包时，只需要执行下面这条命令就可以了。

```
govendor sync
```

`.gitignore` 文件，重点在最后两行：

```
# Created by https://www.gitignore.io/api/go
### Go ###
# Binaries for programs and plugins
*.exe
*.exe~
*.dll
*.so
*.dylib
# Test binary, build with `go test -c`
*.test
# Output of the go coverage tool, specifically when used with LiteIDE
*.out

### Go Patch ###
/vendor/
!/vendor/vendor.json
```
所以，一般的开发流程可以这样来做：如果是新建项目，先安装 govendor 并初始化，然后通过 govendor 来安装依赖包；如果是已有项目，先从版本库拉下来，然后安装 govendor，再执行同步命令即可。

## 其他命令

`govendor status`: 查看当前包状态

`govendor list +e`: 查看当前项目的依赖但是未被添加到 `vendor` 中的包

`govendor add +e`: 添加依赖的包。如果 `vendor.json` 中存在，但是 `vendor` 目录下不存在（即 `govendor status` 显示缺失）的包也会被重新添加

`govendor remove +u`: 删除在 `vendor` 下但是未依赖的包

在实际过程中，有部分包是团队的公共包。 这部分包通常有自己的单独项目，并且已经被我们添加到 `$GOPATH` 下，可能就不需要添加到当前项目的 `vendor` 下。

这时候可以结合 `list` 和 `add` 来使用， 先用 `list -no-status +e` 列出依赖包，然后使用 `grep` 过滤，再调用 `add` 命令添加：

```
govendor list -no-status +e | grep -v 'myteam/common' | xargs govendor add
```


<br>相关文档：<br>
https://github.com/kardianos/govendor<br>
https://www.orztu.com/post/using-govendor/<br>
https://linkscue.com/2018/08/09/2018-08-09-govendor-tips/