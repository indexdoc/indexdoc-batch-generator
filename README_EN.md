<div align="center">
  <div style="font-size: 15px; line-height: 2; padding: 4px 0; letter-spacing: 0.5px;">
    <strong style="color: #24292f;">English</strong>
    | <a href="README.md" style="color: #0969da; text-decoration: none;">简体中文</a>
    | <a href="https://demo.aituple.com/pc/free/index.html?path=batchDoc" target="_blank" style="color: #165DFF; font-weight: 600; text-decoration: none;">✨ onlineDemo</a>
  </div>
  <div style="font-size: 14px; color: #57606a; padding: 2px 0;">
    <span style="background: #f6f8fa; padding: 2px 8px; border-radius: 4px; font-size: 13px;">Core Repos</span>
    <a href="https://github.com/indexdoc/indexdoc-model-to-code" target="_blank" style="color: #0969da; text-decoration: none; margin: 0 6px;">indexdoc-model-to-code（Code Generator / CodeAsst）</a>
    <a href="https://github.com/indexdoc/indexdoc-ai-offline" target="_blank" style="color: #0969da; text-decoration: none; margin: 0 6px;">indexdoc-ai-offline（Local Document AI Assistant）</a>
    <a href="https://github.com/indexdoc/indexdoc-converter" target="_blank" style="color: #0969da; text-decoration: none; margin: 0 6px;">indexdoc-converter（File Converter）</a>
    <a href="https://github.com/indexdoc/indexdoc-editor" target="_blank" style="color: #0969da; text-decoration: none; margin: 0 6px;">indexdoc-editor（Markdown Editor）</a>
    <a href="https://github.com/indexdoc/indexdoc-vector" target="_blank" style="color: #0969da; text-decoration: none; margin: 0 6px;">indexdoc-vector（Vector Database）</a>
  </div>
</div>

---
# Batch Document Assistant
Batch Document Assistant is an efficient document batch generation tool that supports uploading Excel and Word files. You can define the naming rules for the final generated documents via Excel, as well as the fields to be replaced in the Word template. In the Word template, simply mark the content to be replaced in the format of `{column name}` (where the column name corresponds to the column name in the Excel file). After completing the settings, click the generate button to quickly batch generate documents that meet your needs—greatly reducing the time cost of manual editing and replacement, and improving document generation efficiency.

[![Python Version](https://img.shields.io/badge/python-3.10+-green.svg)](https://www.python.org/)  [![GitHub Stars](https://img.shields.io/github/stars/indexdoc/indexdoc-batch-generator?style=social)](https://github.com/indexdoc/indexdoc-batch-generator.git)   [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
![Main Page 1](https://github.com/indexdoc/indexdoc-batch-generator/raw/main/README/mainPage1.png)
After clicking "Generate All", Word files will be batch generated according to the content in the Excel file.
![Main Page 2](https://github.com/indexdoc/indexdoc-batch-generator/raw/main/README/mainPage2.png)
The column names starting from the second column in the Excel file correspond to the content in `{}` in the Word file. After clicking "Generate All", the content of each row will be filled into the Word document according to the column names.
### Sample Files
![Excel Sample File](https://github.com/indexdoc/indexdoc-batch-generator/raw/main/README/excelExampleFlie.png)
![Word Sample File](https://github.com/indexdoc/indexdoc-batch-generator/raw/main/README/wrodExampleFlie.png)
#### Example of Generated Files:

![Generated File Example](https://github.com/indexdoc/indexdoc-batch-generator/raw/main/README/generatedExampleFile.png)

### Frequently Asked Questions
1. **Placeholders not replaced after document generation**: Check if the Excel column names are exactly the same (including case) as the placeholder column names in the Word template;
2. **Generation failure prompt**: Check if the Excel file contains a "Filename" column, or if the filename contains special characters;
3. **Partial documents fail to generate**: Check if the data in the corresponding row is complete, or if the Word template is corrupted


## 📞 Contact Information

- Author: Hangzhou Zhiyu Shu Information Technology Co., Ltd.
- Email: indexdoc@qq.com
- Official Website: https://www.indexdoc.com/
