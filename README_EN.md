<div align="center">
  <strong>English</strong> | <a href="README.md">简体中文</a>
</div>

---
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
```bash
# Install dependencies quickly
pip install -r requirements.txt

# Use Alibaba Cloud PyPI mirror (faster installation)
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
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
