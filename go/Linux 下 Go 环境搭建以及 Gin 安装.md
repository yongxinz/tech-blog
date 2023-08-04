# Linux 下 Go 环境搭建以及 Gin 安装

在 https://golang.org/dl/ 下载 Go 安装包。

将安装包解压：
```
tar -C /usr/local -xzf go1.11.4.linux-amd64.tar.gz
```

修改环境变量：
```
export PATH=$PATH:/usr/local/go/bin
```

此时，Go 就已经安装好了，来验证一下：
```
[root@7a7120c97a4f go]# go version
go version go1.11.4 linux/amd64
```

接下来新建一个名为 test 的项目，目录结构如下：
```
test/
|-- install.sh
`-- src/
```

`install.sh` 文件内容如下：
```sh
#!/usr/bin/env bash

if [ ! -f install.sh ]; then
    echo 'install must be run within its container folder' 1>&2
    exit 1
fi

CURDIR=`pwd`
OLDGOPATH="$GOPATH"
export GOPATH="$CURDIR"

gofmt -w src
go install test

export GOPATH="$OLDGOPATH"
echo 'finished'
```
之所以加上 `install.sh`，而不配置 `GOPATH`，是为了避免新增一个 Go 项目就要往 `GOPATH` 中添加一个路径。这在我们平时练习或者测试，需要新建一个临时项目时很有用。

在 src 目录下新建两个程序，目录结构如下：
```
test/
|-- install.sh
`-- src/
    |-- config
    |   `-- config.go
    `-- test
        `-- main.go
```

程序内容分别是：
```go
// config.go

package config

func LoadConfig(){
}
```

```go
// main.go

package main

import (
    "config"
    "fmt"
)

func main(){
    config.LoadConfig()
    fmt.Println("Hello,GO!")
}
```

然后在项目根目录执行 `sh install.sh`，再看一下项目目录，变成如下结构：
```
test
|-- bin
|   `-- test
|-- install
|-- pkg
|   `-- linux_amd64
|       `-- config.a
`-- src
    |-- config
    |   `-- config.go
    `-- test
        `-- main.go
```
其中 `config.a` 是包 config 编译后生成的；`bin/test` 是生成的可执行的二进制文件。

执行 `bin/test`，输出结果为 `Hello,GO!`。

一般的开发测试流程都可以采用这样的方式，下面来安装 Gin 框架。

```
go get -u github.com/gin-gonic/gin
```

修改 `main.go` 如下：
```go
package main

import (
	"config"
	"fmt"
	
	"github.com/gin-gonic/gin"
)

func main(){
	config.LoadConfig()
	fmt.Println("Hello,GO1!")
	
	r := gin.Default()
    r.GET("/ping", func(c *gin.Context) {
        c.JSON(200, gin.H{
            "message": "pong",
        })
    })
    r.Run() // listen and serve on 0.0.0.0:8080
}

```
简单快捷，只需要执行 `go run main.go`，然后在浏览器中就可以访问了，如果看到 `{"message":"pong"}`，就说明我们的 web 服务已经启动成功了。

这篇文章只是一个简单示例，还有很多功能需要去探索。