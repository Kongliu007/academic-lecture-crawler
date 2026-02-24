## Academic Lecture Crawler

爬取北大与清华物理系的学术讲座信息，输出为 JSON 文件，方便进一步检索与展示。

### 功能特性

- **北大物理学院讲座**：从多个栏目抓取（物院论坛、百年物理讲堂等）
- **清华物理系讲座**：抓取物理系讲座列表
- **统一数据结构**：`school / subject / type / title / speaker / time / location / link`
- **时间过滤**：只保留「今天及之后」的讲座

### 环境与安装

1. 安装依赖（建议使用虚拟环境）：

   ```bash
   cd crawler
   pip install -r requirements.txt
   ```

2. 需要 Python 3.8+。

### 使用方法

在项目根目录（与 `crawler/`、`data/` 同级）执行：

```bash
cd crawler
python -m crawler.run
```

脚本会依次抓取：

- 北大物理学院讲座并保存到 `data/pku/physics.json`
- 清华物理系讲座并保存到 `data/thu/physics.json`

