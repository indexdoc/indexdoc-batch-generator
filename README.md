<div align="center">
  <strong>简体中文</strong> |  <a href="README_EN.md">English</a>
</div>

---
# 批量文档助手
批量文档助手是一款高效便捷的文档批量生成工具，支持上传Excel文件与Word文件，可通过Excel文件定义最终生成文档的文件名规则，以及Word模板中需替换的相关字段；在Word模板中，只需将待替换内容以“{列名}”（列名为Excel文件中的对应列名）的形式标注，完成设置后点击生成按钮，即可快速批量生成符合需求的文档，大幅节省手动编辑、替换文档的时间成本，提升文档生成效率。

[![Python Version](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/)  [![GitHub Stars](https://img.shields.io/github/stars/indexdoc/indexdoc-batch-generator?style=social)](https://github.com/indexdoc/indexdoc-batch-generator.git)   [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ 核心功能

- 🚀 **批量文档生成**：基于 Excel 数据和 Word 模板，一键批量生成自定义文档，支持多字段精准替换

- 📋 **灵活命名规则**：通过 Excel 列定义最终生成文档的文件名，支持组合列名、固定文本等命名方式

- 📝 **简单模板标注**：Word 模板仅需以 `{列名}` 标注待替换内容，无需复杂语法，上手即用

- 📱 **轻量化设计**：纯 Python 实现，无需复杂环境依赖，支持 Windows/macOS/Linux 多系统运行

- 🔧 **容错机制**：内置数据校验、文件格式验证，支持异常提示与日志输出，避免生成失败

- 🛠️ **自定义扩展**：开放核心替换逻辑，支持二次开发（如新增文件格式、自定义替换规则）

##  🚀快速开始

### 环境准备
- Python 3.10+、Tornado 6.0+、ClickHouse 22.0+
- 浏览器：Chrome、Firefox、Edge等主流浏览器。

```bash
https://github.com/indexdoc/indexdoc-batch-generator.git
```
```bash
#快速安装依赖库
pip install -r requirements.txt

# 阿里镜像源
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### 配置
### 后端核心配置（config.py）
| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `port` | int | `50003` | 后端服务运行端口 |
| `ck_config` | dict | `{'host':'127.0.0.1','port':'9000','user':'default','password':'','database':'default'}` | ClickHouse数据库连接配置，包含地址、端口、用户名、密码、数据库名 |
| `max_workers` | int | `16` | 线程池最大线程数量，用于异步任务处理 |
| 路径配置 | string | - | 包含`html_path`（前端页面路径）、`tmp_path`（临时文件路径）、`rpt_path`（报表路径）、`user_file_path`（用户上传文件路径）、`log_path`（日志文件路径），程序启动时自动创建不存在的目录 |
| 日志配置 | - | - | 日志输出格式为`%(asctime)s:%(levelname)s:FILE(%(filename)s %(funcName)s %(lineno)d):%(message)s`，输出到控制台和按天轮转的日志文件（保留365天），日志级别为INFO |
### 数据库文件目录
```bash
sql/create_ck_table.sql
```
### 启动服务
```bash
cd src  # 替换为server.py实际所在的文件夹路径
python.exe server.py
```
**访问地址**
 本地访问：`http://127.0.0.1:50003/public/batchDoc.html`



## 📝 使用示例
点击右侧区域即可上传相应Excel/Word文件。点击样例下载可下载相应的样例文件。
![主页1](https://github.com/indexdoc/indexdoc-batch-generator/raw/main/mainPage1.png)
点击全部生成后，即可按照Excel文件中的内容批量生成Word文件。
![主页2](https://github.com/indexdoc/indexdoc-batch-generator/raw/main/mainPage2.png)
Excel文件中从第二列开始的列名与Word文件中 {} 中的内容相对应，点击全部生成后，每行的内容都会根据列名 填入Word文档中。
### 样例文件
![excel示例文件](https://github.com/indexdoc/indexdoc-batch-generator/raw/main/excelExampleFlie.png)
![wrod示例文件](https://github.com/indexdoc/indexdoc-batch-generator/raw/main/wrodExampleFlie.png)
#### 生成的文件示例如下：

![生成的文件示例](https://github.com/indexdoc/indexdoc-batch-generator/raw/main/generatedExampleFile.png)

### 常见问题
1. **文档生成后占位符未替换**：检查Excel列名与Word模板中的占位符列名是否完全一致（含大小写）；
2. **提示生成失败**：检查Excel文件是否包含「文件名」列，或文件名是否包含特殊字符；
3. **部分文档生成失败**：查看对应行的数据是否完整，或Word模板是否损坏


## 📞 联系方式

- 作者：杭州智予数信息技术有限公司

- 邮箱：indexdoc@qq.com
