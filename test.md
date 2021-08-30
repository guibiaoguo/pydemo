使用 = 和 - 标记一级和二级标题

我展示的是一级标题
================

我展示的是二级标题
----------------

使用# 号标记 可以展示 1-6级标题

# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
###### 六级标题


baidu.com  
GOOGLE.com  

DOGEDOGE.COM

GOOGLE.com

字体

*斜体字体*
_斜体字体_

**粗体字体**
__粗体字体__
***粗斜体文本***

___粗斜体字体___

分割线

***

* * *

*****

- - - 

----------

删除线

BAIDU.COM  
GOOGLE.COM  
~~DOGEDOGE.com~~  

下划线

<u>带下划线文本</u>

脚注

创建脚注格式类似这样 [^RUNOOB]。

[^RUNOOB]: 菜鸟教程 -- 学的不仅是技术，更是梦想！！！

* 第一项
* 第二项
* 第三项

+ 第一项
+ 第二项
+ 第三项

- 第一项
- 第二项
- 第三项

1. 第一项
2. 第二项
3. 第三项

1. 第一项
    - 第一项嵌套的第一个元素
    - 第二项嵌套的第二个元素
2. 第二项：
    - 第二项嵌套的第一个元素
    - 第二项嵌套的第二个元素

Markdown 区块

> 区块引用  
> 菜鸟教程  
> 学弟不仅是技术更是梦想  

> 最外部
> > 第一层嵌套
> > > 第二层嵌套
> > > 

> 区块中使用列表  
> 1. 第一项  
> 2. 第二项  
> 
> * 第一项  
> * 第二项  
> * 第三项  

列表中使用区块

* 第一项  
> 菜鸟教程  
> 学的不仅是技术更是梦想  
* 第二项

Markdown 代码
如果是段落上的一个函数或片段的代码可以用反引号把它包起来（`），例如
`print()` 函数

代码区块
代码区块使用 4 个空格或者一个制表符（Tab 键）

    <?php
    echo 'RUNOOB';
    function test() {
        echo 'test'
    }

   www.google.com/
  [runoob]: http://www.runoob.com/

Markdown 图片

> ` ![alt 属性文本](图片地址) `  
> ` ![alt 属性文本](图片地址 "可选标题")`  

* 开头一个感叹号
* 接着一个方括号，里面放上图片的替代文字
* 接着一个普通括号，里面放上图片的网址，最后还可以用引号包住并选择性的'title'属性的文字

![RUNOOB 图标](https://rmt.dogedoge.com/rmt/R7bR-6-aKqN4tpOmfGOXn4c0En95opNk5AWqdj0Eil5W-jrWV4jEm1idY?w=212&h=130)

![RUNOOB 图标](https://rmt.dogedoge.com/rmt/R7bR-6-aKqN4tpOmfGOXn4c0En95opNk5AWqdj0Eil5W-jrWV4jEm1idY?w=212&h=130 "RUNOOB")

| 表头 | 表头 |
| ---- | ---- |
| 单元格 | 单元格 |
| 单元格 | 单元格 | 

* `-: 设置内容和标题栏居右对齐。`  
* `:- 设置内容和标题栏居左对齐。`  
* `:-: 设置内容和标题栏居中对齐。`  

| 左对齐 | 右对齐 | 居中对齐 |
| :--------- | --------: | :------------: |
| 单元格 | 单元格 | 单元格 |
| 单元格 | 单元格 | 单元格 |


| 左对齐 | 右对齐 | 居中对齐 |
| :-----| ----: | :----: |
| 单元格 | 单元格 | 单元格 |
| 单元格 | 单元格 | 单元格 |

| Syntax      | Description | Test Text     |
| :---        |    :----:   |          ---: |
| Header      | Title       | Here's this   |
| Paragraph   | Text        | And more      |

使用 <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>Del</kbd> 重启电脑
### My Great Heading {#custom-id}
~~世界是平坦的。~~ 我们现在知道世界是圆的。  

- [x] Write the press release  
- [ ] Update the website  
- [ ] Contact the media  

去露营了！ :tent: 很快回来。

真好笑！ :joy:

**文本加粗** 
\*\* 正常显示星号 \*\*


$$  
\mathbf{V}_1 \times \mathbf{V}_2 =  \begin{vmatrix} 
\mathbf{i} & \mathbf{j} & \mathbf{k} \\
\frac{\partial X}{\partial u} &  \frac{\partial Y}{\partial u} & 0 \\
\frac{\partial X}{\partial v} &  \frac{\partial Y}{\partial v} & 0 \\
\end{vmatrix}
${$tep1}{\style{visibility:hidden}{(x+1)(x+1)}}
$$  

```mermaid
graph LR
A[方形] -->B(圆角)
    B --> C{条件a}
    C -->|a=1| D[结果1]
    C -->|a=2| E[结果2]
    F[横向流程图]
```

```mermaid
graph TD
A[方形] --> B(圆角)
    B --> C{条件a}
    C --> |a=1| D[结果1]
    C --> |a=2| E[结果2]
    F[竖向流程图]
```

```flow
st=>start: 开始框
op=>operation: 处理框
cond=>condition: 判断框(是或否?)
sub1=>subroutine: 子流程
io=>inputoutput: 输入输出框
e=>end: 结束框
st->op->cond
cond(yes)->io->e
cond(no)->sub1(right)->op
```

```sequence
对象A->对象B: 对象B你好吗?（请求）
Note right of 对象B: 对象B的描述
Note left of 对象A: 对象A的描述(提示)
对象B-->对象A: 我很好(响应)
对象A->对象B: 你真的好吗？
```

```sequence
Title: 标题：复杂使用
对象A->对象B: 对象B你好吗?（请求）
Note right of 对象B: 对象B的描述
Note left of 对象A: 对象A的描述(提示)
对象B-->对象A: 我很好(响应)
对象B->小三: 你好吗
小三-->>对象A: 对象B找我了
对象A->对象B: 你真的好吗？
Note over 小三,对象B: 我们是朋友
participant C
Note right of C: 没人陪我玩
```

```
%% 时序图例子,-> 直线，-->虚线，->>实线箭头
  sequenceDiagram
    participant 张三
    participant 李四
    张三->王五: 王五你好吗？
    loop 健康检查
        王五->王五: 与疾病战斗
    end
    Note right of 王五: 合理 食物 <br/>看医生...
    李四-->>张三: 很好!
    王五->李四: 你怎么样?
    李四-->王五: 很好!
```

```mermaid
%% 语法示例
        gantt
        dateFormat  YYYY-MM-DD
        title 软件开发甘特图
        section 设计
        需求                      :done,    des1, 2014-01-06,2014-01-08
        原型                      :active,  des2, 2014-01-09, 3d
        UI设计                     :         des3, after des2, 5d
    未来任务                     :         des4, after des3, 5d
        section 开发
        学习准备理解需求                      :crit, done, 2014-01-06,24h
        设计框架                             :crit, done, after des2, 2d
        开发                                 :crit, active, 3d
        未来任务                              :crit, 5d
        耍                                   :2d
        section 测试
        功能测试                              :active, a1, after des3, 3d
        压力测试                               :after a1  , 20h
        测试报告                               : 48h
```







