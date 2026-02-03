目前的RemUp项目包含两个部分，一个是RemUp语言编译器，一个是RemUp语言高亮vscode插件。
其中RemUp语言编译器是用Python编写的，主要功能是将RemUp语言文件编译为HTML文件，并提供实时编译和实时预览功能，是PPL大作业的内容。
RemUp语言高亮vscode插件是用Typescript编写的，主要功能是为RemUp语言提供语法高亮和代码片段提示，是自己搓的方便语言使用的内容，这个项目不会止步于提交作业。

RemUp_compiler/                     # RemUp语言编译器源码
├── remup/
│   ├── __init__.py                 # 初始化文件（注意在md文件中`__`会被识别为文件加粗）
│   ├── ast_nodes.py                # 抽象语法树定义
│   ├── lexer.py                    # 词法解析器
│   ├── parser.py                   # 语法解析器
│   ├── html_generator.py           # HTML生成器
│   ├── compiler.py                 # 编译器
│   ├── live_preview.py             # 实时编译功能文件
│   ├── websocket_preview.py        # 实时编译且实时更新预览的功能文件
│   ├── main.py                     # 主程序入口
│   └── cli.py                      # 形式入口
|
├── static/                         # 静态资源
|   └── Logo.svg                   # RemUp语言logo
│   └── css/
│       ├── RemStyle.css            #remup默认css样式文件
│       ├── CompactStyle.css        #remup紧凑样式文件（做笔记的时候更好用）
│       └── DarkTheme.css           #remup夜间模式主题样式文件
|
├── compile_remup.py                # 编译器（将RemUp文件拖入该文件即可在对应文件目录生成html文件）
├── requirements.txt                # 配置文件
├── README.md                       # RemUp编译器的说明文档
├── examples/                       # 示例文件
└── setup.py                        # 安装程序


（将该目录下的RemUp文件夹复制到C:/用户/{用户名}/.vscode/extensions/后重启vscode即可完成插件安装）
vsvode-remup-syntax/                # RemUp语言高亮vscode插件源码
└── RemUp/                          # 插件包
    ├── .vscode/                    # 插件配置文件
    │   └── launch.json             # 插件配置
    ├── syntaxes/                   # 语法定义文件
    │   └── remup.tmLanguage.json   # RemUp语言语法定义文件
    ├── .vscodeignore               # 忽略文件
    ├── CHANGELOG.md                # 日志文件（我没更新）
    ├── language-configuration.json # 语言配置文件（没啥用，为了结构就留着了）
    ├── package.json                # 安装配置文件
    └── README.md                   # 插件说明文档（插件自带的README模板，我没用）