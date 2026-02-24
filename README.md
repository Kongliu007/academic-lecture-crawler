## Academic Lecture Crawler

爬取高校物理学院学术讲座信息的 Python 爬虫，目前支持：

- 北京大学物理学院
- 清华大学物理系

抓取的数据包括讲座类型、标题、报告人、时间、地点和链接，并只保留今天及之后的讲座信息，输出为 JSON 文件，方便进一步检索与展示。

### 功能特性

- **北大物理学院讲座**：从多个栏目抓取（物院论坛、百年物理讲堂等）
- **清华物理系讲座**：抓取物理系讲座列表
- **统一数据结构**：`school / subject / type / title / speaker / time / location / link`
- **时间过滤**：只保留「今天及之后」的讲座
- **易于扩展**：可以扩展到其他学校或学科

### 环境与安装

使用 Python 3.8+，推荐创建虚拟环境。

在项目根目录（与 `crawler/`、`data/` 同级）执行：

```bash
cd crawler
pip install -r requirements.txt
```

### 使用方法

在 `crawler` 目录下运行入口脚本：

```bash
cd crawler
python -m crawler.run
```

脚本会依次抓取：

- 北大物理学院讲座并保存到 `data/pku/physics.json`
- 清华物理系讲座并保存到 `data/thu/physics.json`
