# 前言

一个可以diy的渗透测试集成工具的gui界面，当然其他用途也可以
作为一个安全小白，工具肯定是不会少用的，但是我用了一些安全大佬开发这种类型的工具之后，虽然工具类型很多，但我发现很多工具对于我这种小白来说还没用得上，想自己diy一个，这个工具就出来了，主要是思路加上ai写的，当然也借鉴了大佬们写的工具，希望大家下载使用觉得不错就点一下start吧，谢谢各位师傅，只能windows使用

# 用法
用法很简单，一开始要配置一下启动那里，要是直接运行不行的话，就改一下那个vbs就可以了，还有那个重建脚本也要改一下，里面都有提示的，里面配置了config.py和config.json，一个是gui界面的配置，一个是工具的配置，![image](https://github.com/user-attachments/assets/1293e438-2d82-41a3-9cf2-d8711f089bde)
界面就是这样，要是不喜欢样式可以在config.py那里改样式，还有那个图标也可以改，反正里面都有提示，要是想改就改就可以了
# 功能
讲完界面就讲一下功能吧，<br>![image](https://github.com/user-attachments/assets/811bb0d5-33e8-4c4a-9c13-73bc25d9ab88)<br>
还有工具栏里面都可以改，看代码就可以了<br>
首先讲点击功能
左键点击按钮就能执行工具所在json里面配置好的命令，右键就是打开对应按钮工具的目录，这个功能我个人很喜欢，有时候有些工具会生成文件，每次还要打开文件夹很麻烦，所以就加了这个功能<br>
第二个就讲这个管理工具这个功能，
<br>![image](https://github.com/user-attachments/assets/4f5a3e5a-9c2f-4549-b60e-2e593cf74d86)<br>
这个功能还可以改进，就是不能实时更新gui界面，每次添加完或者删除完要重新进入gui界面才能加载，会改的师傅可以改进一下
我就讲一下他的逻辑吧，我感觉很好用，首先会让你添加到哪一个类别，<br>![image](https://github.com/user-attachments/assets/7f3d77d2-a12c-4f36-a017-795b81a54eca)
<br>
自己选就可以了，下一步就是工具名字，也是写就可以了，下一步这个输入子路径，这个功能是会拼接你输入的路径，<br>首先我建议各位师傅保留我最初的json，因为这个功能是读取第一个路径来拼接的，一般都会把工具放在一个目录的，你选择完类别直接写文件夹名字就可以了，不用写全，就像比如你类别写信息收集，子路径写a/,最后写到json的路径就是信息收集/a,所以个个模块的第一个工具的路径要好好的写，<br>第三个就是选择环境，选python就是命令拼接的时候是python3，选java就是java -jar,当然这些都可以改，师傅们看代码就可以了，然后输入命令数量，然后要输入命令，这里直接写命令就可以了，不用写python3这些，因为前面已经拼接了，我写这个功能的初衷是因为很多工具有很多命令模版，像什么-u -w这些很难记住，所以有这个功能，<br>最后工具会问一下要不要继续添加，回车或者y就是继续添加，我写这个功能主要是因为怕有些师傅直接动手改json的时候会把json格式写错了或者有些时候工具id重复了，用工具添加就会自动加1，工具id是执行命令的唯一标识，必须唯一，
<br>下面讲一下删除的<br>![image](https://github.com/user-attachments/assets/849d94c3-5a2b-473f-b39d-df21a3bce5fc)
<br>删除就是会个根据你的json来显示，你选完之后删除就可以了，后面和上面添加工具的一致<br>
最后来讲一下执行的逻辑也就是tools.py，这个逻辑就是读取你json工具对应的命令，如果是python的命令就会重新打开一个cmd窗口把运行命令的过程给你看，还有会把命令输到cmd里面，要是想改就复制过来改就可以了，如果是java的就会直接打开，exe和bat和java一样
# 手动改工具配置文件
当然也可以直接改json文件，但是每次改完还要运行一次重建脚本.bat，使用gui里面的添加和删除就不用，<br>因为每次添加或者删除自动运行，还有手动添加命令的时候，如果你想打开目录或者运行exe，bat这类文件的时候命令里面写start加上要执行的文件或者路径就可以了<br>通过json直接删除，但好处和不足和添加工具介绍写一样
# 最后
好了工具功能就介绍到这，总的来说工具减少了我们测试的时候一些打开目录或者写一些复杂命令,上面这些功能的思路都是看了很多github上面大佬的gui工具总结和修改出来的，当然这个项目还有很多不足的地方，<br>由于第一次发表，不知道包这个有没有写全，因为我看req那个文件挺少的，要是包没有写全，请师傅们自己下载全，<br>当然有很多bug，比如我没有测试另一台电脑能不能运行，当然一般可以运行，要是有bug请师傅们自行修改或者提建议吧，<br>最后写一下还可以改进的地方，像添加或者删除工具的时候实时更新gui界面，这个可以写一下，还有右键打开目录的时候是重新开一个窗口，可以改成就开一个窗口，要是再打开的话就像手动新建标签页一样，还有很多，就留给师傅们自行修改了
# 工具参考
https://github.com/Hekeatsll/PenKitGui
# 版本更新
```markdown
2024年9月22号 v0.2发布 增加自定义改参数，可以将模版写到那里，然后选择完命令，改对应的值就可以了
2024年9月22号 v0.1发布
```
# 免责声明
```markdown
**1. 工具用途说明：**  
本工具是为合法授权的企业安全建设行为而设计，旨在辅助安全专家和研究人员进行网络安全评估和渗透测试。本工具的使用应严格限制在授权的范围内，并且必须遵守所有适用的法律法规。

**2. 合法使用承诺：**  
在使用本工具进行检测时，您应确保该行为符合当地的法律法规，并且已经取得了足够的授权。本工具不得用于任何非法目的，包括但不限于未经授权的访问、数据窃取、服务中断或其他任何形式的网络攻击。

**3. 法律责任：**  
如您在使用本工具的过程中存在任何非法行为，您需自行承担相应后果，我们将不承担任何法律及连带责任。我们强烈建议用户在使用本工具前，咨询法律顾问，确保其行为的合法性。

**4. 免责声明：**  
- 本工具提供“原样”使用，不提供任何形式的保证，包括但不限于适销性、适用于特定目的或不侵犯第三方权利的保证。
- 使用本工具时，您应自行判断并承担所有风险。我们不对因使用本工具而产生的任何直接、间接、特殊、偶然或惩罚性的损害承担责任，无论这些损害是否可预见。
- 我们不保证本工具的运行不会中断或无错误，也不保证任何缺陷将被纠正。
- 我们不对任何由于使用本工具而造成的数据丢失或损害承担责任。
- 我们不对任何由于本工具的任何缺陷、错误或故障导致的任何类型的损失或损害承担责任，包括但不限于利润损失、业务中断、商业信息的丢失或其他财务损失。

**5. 用户同意：**  
在使用本工具前，请您务必审慎阅读、充分理解各条款内容。限制、免责条款或者其他涉及您重大权益的条款可能会以加粗、加下划线等形式提示您重点注意。除非您已充分阅读、完全理解并接受本协议所有条款，否则，请您不要使用本工具。

**6. 接受协议：**  
您的使用行为或者您以其他任何明示或者默示方式表示接受本协议的，即视为您已阅读并同意本协议的约束。我们保留随时更新本免责声明的权利，更新后的免责声明一旦公布即生效，如您继续使用本工具，即表示您接受更新后的免责声明。
