markdown
<div align="center">
  <strong>简体中文</strong> |  <a href="README_EN.md">English</a>
</div>

---
# 批量文档助手
批量文档助手是一款高效便捷的文档批量生成工具，支持上传Excel文件与Word文件，可通过Excel文件定义最终生成文档的文件名规则，以及Word模板中需替换的相关字段；在Word模板中，只需将待替换内容以“{列名}”（列名为Excel文件中的对应列名）的形式标注，完成设置后点击生成按钮，即可快速批量生成符合需求的文档，大幅节省手动编辑、替换文档的时间成本，提升文档生成效率。

[![Python Version](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/)  [![GitHub Stars](https://img.shields.io/github/stars/indexdoc/indexdoc-batch-generator?style=social)](https://github.com/indexdoc/indexdoc-batch-generator.git) 
# Batch Document Assistant
Batch Document Assistant is an efficient document batch generation tool that supports uploading Excel and Word files. You can define the naming rules for the final generated documents via Excel, as well as the fields to be replaced in the Word template. In the Word template, simply mark the content to be replaced in the format of `{column name}` (where the column name corresponds to the column name in the Excel file). After completing the settings, click the generate button to quickly batch generate documents that meet your needs—greatly reducing the time cost of manual editing and replacement, and improving document generation efficiency.

[![Python Version](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/)  [![GitHub Stars](https://img.shields.io/github/stars/indexdoc/indexdoc-batch-generator?style=social)](https://github.com/indexdoc/indexdoc-batch-generator.git) 

## ✨ Core Features

- 🚀 **Batch Document Generation**: Based on Excel data and Word templates, one-click batch generation of custom documents with support for precise replacement of multiple fields
- 📋 **Flexible Naming Rules**: Define the filenames of the final generated documents via Excel columns, supporting naming methods such as combined column names and fixed text
- 📝 **Simple Template Annotation**: Word templates only need to mark content to be replaced with `{column name}`—no complex syntax required, easy to get started
- 📱 **Lightweight Design**: Pure Python implementation with no complex environment dependencies, supporting multi-system operation (Windows/macOS/Linux)
- 🔧 **Fault Tolerance Mechanism**: Built-in data validation and file format verification, supporting exception prompts and log output to avoid generation failures
- 🛠️ **Custom Extension**: Open core replacement logic, supporting secondary development (e.g., adding new file formats, custom replacement rules)

## 🚀 Quick Start

### Environment Preparation
- Python 3.10+, Tornado 6.0+, ClickHouse 22.0+
- Browsers: Chrome, Firefox, Edge, and other mainstream browsers.

```bash
https://github.com/indexdoc/indexdoc-batch-generator.git
```

### Configuration
### Backend Core Configuration (config.py)
| Configuration Item | Type | Default Value | Description |
|--------------------|------|---------------|-------------|
| `port` | int | `50003` | Port for backend service operation |
| `ck_config` | dict | `{'host':'127.0.0.1','port':'9000','user':'default','password':'','database':'default'}` | ClickHouse database connection configuration, including address, port, username, password, and database name |
| `max_workers` | int | `16` | Maximum number of threads in the thread pool, used for asynchronous task processing |
| Path Configuration | string | - | Includes `html_path` (frontend page path), `tmp_path` (temporary file path), `rpt_path` (report path), `user_file_path` (user uploaded file path), `log_path` (log file path). Non-existent directories are automatically created when the program starts |
| Log Configuration | - | - | Log output format is `%(asctime)s:%(levelname)s:FILE(%(filename)s %(funcName)s %(lineno)d):%(message)s`, output to the console and daily rotated log files (retained for 365 days), log level is INFO |
### Database File Directory
```bash
sql/create_ck_table.sql
```
### Start the Service
```bash
cd src  # Replace with the folder path where server.py is actually located
python.exe server.py
```
**Access Address**
Local access: `http://127.0.0.1:50003/public/batchDoc.html`



## 📝 Usage Example
Click the right area to upload the corresponding Excel/Word files. Click "Download Sample" to download the corresponding sample files.
![Main Page 1](https://github.com/indexdoc/indexdoc-batch-generator/raw/main/mainPage1.png)
After clicking "Generate All", Word files will be batch generated according to the content in the Excel file.
![Main Page 2](https://github.com/indexdoc/indexdoc-batch-generator/raw/main/mainPage2.png)
The column names starting from the second column in the Excel file correspond to the content in `{}` in the Word file. After clicking "Generate All", the content of each row will be filled into the Word document according to the column names.
### Sample Files
![Excel Sample File](https://github.com/indexdoc/indexdoc-batch-generator/raw/main/excelExampleFlie.png)
![Word Sample File](https://github.com/indexdoc/indexdoc-batch-generator/raw/main/wrodExampleFlie.png)
#### Example of Generated Files:

![Generated File Example](https://github.com/indexdoc/indexdoc-batch-generator/raw/main/generatedExampleFile.png)

### Frequently Asked Questions
1. **Placeholders not replaced after document generation**: Check if the Excel column names are exactly the same (including case) as the placeholder column names in the Word template;
2. **Generation failure prompt**: Check if the Excel file contains a "Filename" column, or if the filename contains special characters;
3. **Partial documents fail to generate**: Check if the data in the corresponding row is complete, or if the Word template is corrupted


## 📞 Contact Information

- Author: Hangzhou Zhiyu Shu Information Technology Co., Ltd.
- Email: indexdoc@qq.com
- Official Website: https://www.indexdoc.com/


要不要我帮你整理一份**中英文版本的切换链接代码**，方便你添加到主 README 中？
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

- 官方网站：https://www.indexdoc.com/
