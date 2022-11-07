![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/0.png)

**原文链接：** [Git 分支管理策略](https://mp.weixin.qq.com/s/hRd1UNMRutmA6MGmswweBw)

最近，团队新入职了一些小伙伴，在开发过程中，他们问我 Git 分支是如何管理的，以及应该怎么提交代码？

我大概说了一些规则，但仔细想来，好像也并没有形成一个清晰规范的流程。所以查了一些资料，总结出下面这篇文章，分享给大家。

## Git flow

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/11.png)

在这种模式下，主要维护了两类分支：

- 主要分支 (The main branch)
  - master
  - develop
- 辅助分支 (Supporting branch)
  - feature branch (功能分支)
  - release branch (预发布分支)
  - hotfix branch (热修复分支)

### master

首先，代码库应该有一个、且仅有一个主分支。master 分支的代码永远是稳定的，可以随时发布到生产环境。

### develop

develop 分支用于日常开发，保存了开发过程中最新的代码。

当 develop 分支上的代码达到稳定，并且具备发版状态时，需要将 develop 的代码合并到 master，并且打一个带有发布版本号的 tag。

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/2.png)

创建 develop 分支：

```shell
git checkout -b develop master
```

将 develop 合并到 master：

```shell
# 切换到 master 分支
git checkout master

# 对 develop 分支进行合并
git merge --no-ff develop
```

`--no-ff` 参数的作用是使当前的合并操作总是创建一个新的 commit 对象，即使该合并被执行为快进式（fast-forward）合并。

这样可以避免丢失掉该功能分支的历史信息，并且将针对该功能的所有提交都集中到一起。这样解释也并不是很易懂，通过下图来对比一下就比较明显了：

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/3.png)

### feature

- 分支来源：develop
- 合并到分支：develop
- 分支命名约定：feature-*

功能分支，在开发某一个新功能时，从 develop 分支分出来，开发完之后，再合并回 develop 分支。

功能分支通常只存在于开发者的本地仓库中，并不包含在远程库中。

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/4.png)

创建一个功能分支：

```shell
git checkout -b feature-x develop
```

开发完成后，将功能分支合并到 develop 分支：

```shell
git checkout develop

git merge --no-ff feature-x
```

删除 feature 分支：

```shell
git branch -d feature-x
```

### release

- 分支来源：develop
- 合并到分支：develop，master
- 分支命名约定：release-*

预发布分支，它是指发布正式版本之前，我们可能需要有一个预发布的版本测试，并且可以在上面做一些较小 bug 的修复。

预发布分支是从 develop 分支上分出来的，预发布结束以后，必须合并进 develop 和 master 分支。

创建一个预发布分支：

```shell
git checkout -b release-1.2 develop
```

确认没有问题后，合并到 master 分支：

```shell
git checkout master

git merge --no-ff release-1.2

# 对合并生成的新节点，做一个标签
git tag -a 1.2
```

再合并到 develop 分支：

```shell
git checkout develop

git merge --no-ff release-1.2
```

最后，删除预发布分支：

```shell
git branch -d release-1.2
```

### hotfix

- 分支来源：master
- 合并到分支：develop，master
- 分支命名约定：hotfix-*

最后一种是修复 bug 分支。软件正式发布以后，难免会出现 bug。这时就需要创建一个分支，进行 bug 修复。

修复 bug 分支是从 master 分支上分出来的。修复结束以后，再合并进 master 和 develop 分支。

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/5.png)

创建一个修复 bug 分支：

```shell
git checkout -b hotfix-0.1 master
```

修复结束后，合并到 master 分支：

```shell
git checkout master

git merge --no-ff hotfix-0.1

git tag -a 0.1.1
```

再合并到 develop 分支：

```shell
git checkout develop

git merge --no-ff hotfix-0.1
```

最后，删除修复 bug 分支：

```shell
git branch -d hotfix-0.1
```

### 小结

**优点：** 

1. 各分支权责分明，清晰可控，是很多分支管理策略的启蒙模型。

**缺点：**

1. 合并冲突：同时长期存在的分支可能会很多：master、develop、release、hotfix、若干并行的 feature 分支。两两之间都有可能发生冲突。频繁手动解决冲突不仅增加工作量，而且增大了出错的风险。
2. 功能分离：功能并行开发时，合并分支前无法测试组合功能，而且合并后可能会出现互相影响。
3. 无法持续交付：Git flow 更倾向于按计划发布，一个 feature 要经历很多步骤才能发布到正式环境，难以达到持续交付的要求。
4. 无法持续集成：持续集成鼓励更加频繁的代码集成和交互，尽早解决冲突，而 Git flow 的分支策略隔离了代码，尽可能推迟代码集成。

## Github flow

Github flow 是一个轻量级的基于分支的工作流程。它由 GitHub 在 2011 年创建。分支是 Git 中的核心概念，并且 GitHub 工作流程中的一切都以此为基础。

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/6.png)

它只有一个长期分支 master，其他分支都在其基础上创建。使用流程如下：

1. 根据需求，从 master 拉出新分支，不用区分功能分支或修复分支，但需要给出描述性的名称。
2. 本地的修改直接提交到该分支，并定期将其推送到远程库上的同一命名分支。
3. 新分支开发完成后，或者需要讨论的时候，向 master 发起一个 Pull Request（简称 PR）。
4. Pull Request 既是一个通知，让别人注意到你的请求，又是一种对话机制，大家一起评审和讨论你的代码。对话过程中，你还可以不断提交代码。
5. 你的 Pull Request 被接受，合并进 master，重新部署后，原来你拉出来的那个分支就被删除了。

### 小结：

**优点：**

1. 降低了分支管理复杂度，更适合小型团队，或者维护单个版本的项目开发。
2. 工作流程简单，对持续交付和持续集成友好。


**缺点：**

1. 无法支持多版本代码部署。

## Gitlab flow

它是 Git flow 与 Github flow 的综合。吸取了两者的优点，既有适应不同开发环境的弹性，又有单一主分支的简单和便利。

Gitlab flow 和 Github flow 之间的最大区别是 Gitlab flow 支持环境分支。

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/7.png)

Gitlab flow 的最大原则叫做"上游优先"（upsteam first），即只存在一个主分支 master，它是所有其他分支的"上游"。只有上游分支采纳的代码变化，才能应用到其他分支。

Gitlab flow 分成两种情形来应付不同的开发流程：

- 持续发布
- 版本发布

### 持续发布

对于持续发布的项目，它建议在 master 分支以外，再建立不同的环境分支，每个环境都有对应的分支。比如，开发环境的分支是 master，预发环境的分支是 pre-production，生产环境的分支是 production。

- 开发分支 master 用于发布到测试环境，该分支为受保护的分支。
- 预发分支 pre-production 用于发布到预发环境，上游分支为 master。
- 正式分支 production 用于发布到正式环境，上游分支为 pre-production。

如果生产环境（production）发生错误，则要建一个新分支修改完后合并到最上游的开发分支（master）此时就是（Upstream first），且经过测试，再继续往 pre-production 合并，要经过测试没有问题了才能够再往下合并到生产环境。

### 版本发布

对于版本发布的项目，建议的做法是每一个稳定版本，都要从 master 分支拉出一个分支，比如 2-3-stable、2-4-stable 等。

在出现 bug 后，根据对应的 release branch 创建一个修复分支，修复工作完成后，一样要按照上游优选的原则，先合并到 master 分支，经过测试才能够合并到 release 分支，并且此时要更新小版本号。

### 小结

**优点：**

1. 可以区分不同的环境部署。
2. 对持续交付和持续集成友好。


**缺点：**

1. 分支多，流程管理复杂。

## TrunkBased

Trunk Based Development，又叫**主干开发**。开发人员之间通过约定，向被指定为主干，一般为 master，的分支提交代码，以此来抵抗因为长期存在的多分支导致的开发压力。这样可以避免分支合并的困扰，保证随时拥有可发布的版本。

![](https://cdn.jsdelivr.net/gh/yongxinz/picb@main/8.jpeg)

使用主干开发后，只有一个 master 分支了，所有新功能也都提交到 master 分支上，保证每次提交后 master 分支都是可随时发布的状态。

没有了分支的代码隔离，测试和解决冲突都变得简单，持续集成也变得稳定了许多，但也有如下几个问题：

- 如何避免发布的时候引入未完成的 feature
- 如何进行线上 bug fix

### 如何避免发布的时候引入未完成的 feature

答案是：[Feature Toggle](https://martinfowler.com/articles/feature-toggles.html)。

既然代码要随时保持可发布，而我们又需要只有一份代码来支持持续集成，在代码库里加一个特性开关来随时打开和关闭新特性是最容易想到的，当然也是最容易被质疑的解决方案。

Feature Toggle 是有成本的，不管是在加 Toggle 的时候的代码设计，还是在移除 Toggle 时的人力成本和风险，都是需要和它带来的价值进行衡量的。

事实上，在我们做一个前端的大特性变更的时候，我们确实因为没办法 Toggle 而采用了一个独立的 feature 分支，我们认为即使为了这个分支单独做一套 Pipeline，也比在前端的各种样式间添加移除 Toggle 来得简单。

但同时，团队商议决定在每次提交前都要先将 master 分支合并到 feature 分支，以此避免分支隔离久以后合并时的痛苦。

### 如何进行线上 bug fix

在发布时打上 release tag，一旦发现这个版本有问题，如果这个时候 master 分支上没有其他提交，可以直接在 master 分支上 hot fix，如果 master 分支已经有了提交就要做以下四件事：

1. 从 release tag 创建发布分支。
2. 在 master 上做 bug fix 提交。
3. 将 bug fix 提交 cherry-pick 到 release 分支。
4. 在 release 分支再做一次发布。

线上 fix 通常都比较紧急。看完这个略显繁琐的 bug fix 流程，你可能会问为什么不在 release 分支直接 fix，再合并到 master 分支？

这样做确实比较符合直觉，但事实是，如果在 release 分支做 fix，很可能会忘了合并回 master。

试想深夜两点你做完 bug fix 眼看终于上线成功，这时你的第一反应就是“终于可以下班了。什么，合并回 master？ 明天再来吧“ 

等到第二天你早已把这个事忘得一干二净。而问题要等到下一次上线才会被暴露出来，一旦发现，而这个时候上一次 release 的人又不在，无疑增加了很多工作量。

## 总结

以上四种就是目前相对主流的分支管理策略，但没有哪一种策略是万能的。所以无论选择哪一种，都需要考虑团队的实际情况，以及项目的具体业务需求，适合自己的才是最好的。

最后，再分享三点小建议：

1. 临时分支不应该存在太久，每个分支应尽量保持精简，用完即删
2. 工作流应该尽量简单，同时方便回滚
3. 工作流程应该符合我们的项目发布计划

以上就是本文的全部内容，如果觉得还不错的话欢迎**点赞**，**转发**和**关注**，感谢支持。

---

**参考文章：**

- [Git 分支管理策略与工作流程](https://www.liuxing.io/blog/git-workflow/#gitlab-flow-%E5%B7%A5%E4%BD%9C%E6%B5%81)
- [Git 分支管理策略总结](https://juejin.cn/post/6844904203115036685#heading-3)
- [一个完美的 Git 分支管理模型](http://matrixzk.github.io/blog/20141104/git-flow-model/#section-5)
- [Git 工作流程](http://www.ruanyifeng.com/blog/2015/12/git-workflow.html)
- [Git 分支管理策略](https://www.ruanyifeng.com/blog/2012/07/git.html)
- [分支模型与主干开发](https://www.duyidong.com/2017/10/29/trunk-base-development/#Github-Flow)

**扩展阅读：**

- [在阿里，我们如何管理代码分支？](https://developer.aliyun.com/article/573549)
- [谷歌的代码管理](http://www.ruanyifeng.com/blog/2016/07/google-monolithic-source-repository.html)

**推荐阅读：**

- [Go 学习路线（2022）](https://mp.weixin.qq.com/s/Dwf98JFUnRij0Ha7o3ZSHQ)
- [**Python 学习路线（2022）**](https://mp.weixin.qq.com/s/CyJ92-CD1xnihlp-Dqj8Yw)
- [本着什么原则，才能写出优秀的代码？](https://mp.weixin.qq.com/s/xWZmP4qBI8cm68UZH6AXOg)
