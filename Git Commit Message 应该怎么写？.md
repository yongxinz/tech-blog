**原文链接：** [Git Commit Message 应该怎么写？](https://mp.weixin.qq.com/s/EvN_lUyiQnlHR9kJ5SiosA)

最近被同事吐槽了，说我代码提交说明写的太差。其实都不用他吐槽，我自己心里也非常清楚。毕竟很多时候犯懒，都是直接一个 `-m "fix"` 就提交上去了。

这样做是非常不好的，我也是自食恶果，深受其害。特别是查看历史提交记录时，想通过提交说明来了解当时的功能变更，基本不可能，都得点进去看代码才行。

所以这两天看了一些**如何写好提交说明**的资料，系统地学习了一下。虽然团队没有这方面的要求，但是想要进步，得对自己提更高的要求才行。

一般使用 git 提交代码的话，可以使用 `-m` 参数来指定提交说明，比如：

```shell
$ git commit -m "hello world"
```

如果一行不够，可以只执行 `git commit`，这样就会跳出文本编辑器来写多行：

```shell
$ git commit
```

## Commit Message 格式

Commit Message 包括三个部分：Header，Body 和 Footer。

```shell
<Header>

<Body>

<Footer>
```

其中，Header 是必需的，Body 和 Footer 可以省略。

### Header

Header 部分只有一行，包括三个字段：type（必需）、scope（可选）、subject（必需）。

```shell
<type>(<scope>): <subject>
```

#### type

type 用于说明 commit 的类别，具体的标识如下：

- `feat`：一个新的功能（feature）；
- `fix`：修复 bug;
- `docs`：修改文档，比如 README.md、CHANGELOG.md 等；
- `style`：修改代码的格式，不影响代码运行的变动，比如空格、格式化代码、补齐句末分号等等；
- `refactor`：代码重构，没有新功能的添加以及 bug 修复的代码改动；
- `perf`：优化代码以提高性能；
- `test`：增加测试或优化改善现有的测试；
- `build`：修改影响项目构建文件或外部依赖项，比如 npm、gulp、webpack、broccoli 等；
- `ci`：修改 CI 配置文件和脚本；
- `chore`：其他非 src 路径文件和测试文件的修改，比如 .gitignore、.editorconfig 等；
- `revert`：代码回退；

#### scope

scope 用于说明 commit 的影响范围，比如数据层、控制层、视图层等等，视项目不同而不同。

如果你的修改影响了不止一个 scope，就可以使用 `*` 代替。

#### subject

subject 是 commit 目的的简单描述，不超过 50 个字符，结尾不需要句号。

### Body

Body 部分是对本次 commit 的详细描述，可以分多行。

Body 部分应该说明代码变动的动机，以及与以前行为的对比。

```shell
More detailed explanatory text, if necessary.  Wrap it to
about 72 characters or so.

Further paragraphs come after blank lines.

- Bullet points are okay, too
- Use a hanging indent
```

### Footer

Footer 部分主要用于两种情况：不兼容变动和处理 Issue。

#### 不兼容变动

如果当前代码与上一个版本不兼容，则 Footer 部分以 `BREAKING CHANGE:` 开头，后面就是对变动的描述、以及变动理由和迁移方法。

```shell
BREAKING CHANGE: Previously, $compileProvider.preAssignBindingsEnabled was set to true by default. This means bindings were pre-assigned in component constructors. In Angular 1.5+ the place to put the initialization logic relying on bindings being present is the controller $onInit method.

To migrate follow the example below:

Before:

​```js
angular.module('myApp', [])
    .component('myComponent', {
        bindings: {value: '<'},
        controller: function() {
        this.doubleValue = this.value * 2;
    }
});
​```

After:
​```js
angular.module('myApp', [])
    .component('myComponent', {
        bindings: {value: '<'},
        controller: function() {
            this.$onInit = function() {
                this.doubleValue = this.value * 2;
            };
        };
        this.doubleValue = this.value * 2;
    }
});
​```

Don't do this if you're writing a library, though, as you shouldn't change global configuration then.
```

#### 处理 Issue

处理 Issue 分为两种情况，分别是关联 Issue 和关闭 Issue。

比如本次提交如果和某个 issue 有关系：

```shell
Issue #1, #2, #3
```

如果当前提交信息解决了某个 issue：

```shell
Close #1, #2, #3
```

### Revert

还有一种特殊情况，如果当前 commit 用于撤销以前的 commit，则必须以 `revert:` 开头，后面跟着被撤销 commit 的 Header。

```shell
revert: feat(pencil): add 'graphiteWidth' option

This reverts commit 667ecc1654a317a13331b17617d973392f415f02.
```

Body 部分的格式是固定的，必须写成 `This reverts commit &lt;hash>.`，其中 hash 是被撤销 commit 的 SHA 标识符。

如果当前 commit 与被撤销的 commit，在同一个发布（release）里面，那么它们都不会出现在 Change log 里面。如果两者在不同的发布，那么当前 commit，会出现在 Change log 的 Reverts 小标题下面。

最后来看一个例子，算是一个总结，至于具体内容还是要根据实际情况来填写。

```shell
feat: 添加了分享功能

给每篇博文添加了分享功能

- 添加分享到微博功能
- 添加分享到微信功能
- 添加分享到朋友圈功能

Issue #1, #2
Close #1
```

## 插件推荐

有了这些规范，也知道怎么写了，但是不是会担心记不住呢？不要怕，有插件可以用，如果使用 VsCode 的话，可以安装一个叫 **Commit Message Editor** 的插件。

可以根据提示信息直接写：

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/workflow/preview1.gif)

也可以使用表单的方式，有选项可以选择：

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/workflow/preview2.gif)

这样不仅可以很方便地写提交说明了，还可以使提交说明更加的规范。

以上就是本文的全部内容，如果觉得还不错的话欢迎**点赞**，**转发**和**关注**，感谢支持。

---

**参考文章：**

- https://juejin.cn/post/6960541430473293837
- https://mrseawave.github.io/blogs/articles/2021/03/31/git-commit-message/

**推荐阅读：**

- [Git 分支管理策略](https://mp.weixin.qq.com/s/hRd1UNMRutmA6MGmswweBw)