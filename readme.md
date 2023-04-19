<!-- omit in toc -->

# Awesome DICOM [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of awesome DICOM resources and libraries.

The [DICOM Standard](https://www.dicomstandard.org/) is _the_ international standard for medical images and related information. It defines the formats for medical images that can be exchanged with the data and quality necessary for clinical use <sup>[[source](https://www.dicomstandard.org/about-home)]</sup>.

<!-- omit in toc -->

## Contents

- [Learning Resources](#learning-resources)
- [Libraries](#libraries)
  - [C#](#c)
  - [C++](#c-1)
  - [Go](#go)
  - [Java](#java)
  - [JavaScript](#javascript)
  - [MATLAB](#matlab)
  - [Python](#python)
  - [Rust](#rust)
  - [Other/Combination](#othercombination)
- [Contribute](#contribute)

## Learning Resources

- [The DICOM Standard](https://www.dicomstandard.org/current)
- [DICOM Library](https://www.dicomlibrary.com/) - A free online medical DICOM image or video file sharing service for educational and scientific purposes.
- [DICOM Standard Browser](https://dicom.innolitics.com/ciods) - Part 3 of the DICOM standard as a tree.
- [DICOM is Easy](https://dicomiseasy.blogspot.com/2011/10/introduction-to-dicom-chapter-1.html) - A personal blog which includes a series of DICOM tutorials.
- [Microsoft training module](https://learn.microsoft.com/en-us/training/modules/medical-imaging-data/) - Short training module about working with medical imaging data in general and DICOM in particular.
- [Saravanan Subramanian's blog](https://saravanansubramanian.com/dicomtutorials/) - A series of articles and tutorials focusing on working with DICOM using Java and .NET.

## Libraries

### C#

#### General

- [dicom-server](https://github.com/microsoft/dicom-server) - The Medical Imaging Server for DICOM is an open source DICOM server that is easily deployed on Azure.
- [DICOMcloud](https://github.com/DICOMcloud/DICOMcloud) - A standalone DICOMWeb server with RESTful implementation of the DICOMWeb/WADO services. The DICOMcloud server can interface with any DICOMWeb client over the current implemented features (qido-rs, wado-uri, wado-rs and stow-rs).
- [Evil-DICOM](https://github.com/rexcardan/Evil-DICOM) - A simple to use library for reading and manipulating DICOM files.
- [fo-dicom](https://github.com/fo-dicom/fo-dicom) - Fellow Oak DICOM, a DICOM toolkit in C# for all .NET Standard 2.0 compatible frameworks.

#### Visualization

- [UnityVolumeRendering](https://github.com/mlavik1/UnityVolumeRendering) - A volume renderer, made with Unity3D.

### C++

#### General

- [CTK](https://github.com/commontk/CTK) - The Common Toolkit is a community effort to provide support code for medical image analysis, surgical navigation, and related projects.
- [DCMTK](https://github.com/DCMTK/dcmtk) - The DICOM ToolKit (DCMTK) package consists of source code, documentation and installation instructions for a set of software libraries and applications implementing part of the DICOM/MEDICOM Standard.
- [dcmqi](https://github.com/QIICR/dcmqi) - DICOM for Quantitative Imaging (dcmqi) is a collection of libraries and command line tools with minimum dependencies to support standardized communication of quantitative image analysis research data using the DICOM standard.
- [GDCM](https://github.com/malaterre/GDCM) - Grassroots DICOM (GDCM) is an implementation of the DICOM standard designed to be open source, so that researchers may access clinical data directly. GDCM includes a file format definition and a network communications protocol, both of which should be extended to provide a full set of tools for a researcher or small medical imaging vendor to interface with an existing medical database.
- [MITK](https://github.com/MITK/MITK) - The Medical Imaging Interaction Toolkit (MITK) is a free open-source software system for development of interactive medical image processing software. MITK combines the Insight Toolkit (ITK) and the Visualization Toolkit (VTK) with an application framework.
- [Orthanc](https://github.com/jodogne/OrthancMirror) - A simple yet powerful standalone DICOM server. It is designed to improve the DICOM flows in hospitals and to support research about the automated analysis of medical images.
- [SimpleITK](https://github.com/SimpleITK/SimpleITK) - A simplified interface for the Insight Toolkit [ITK](https://itk.org/) with several components supporting general filtering operations, image segmentation, and registration.
- [vtk-dicom](https://github.com/dgobbi/vtk-dicom) - A set of classes for managing DICOM files and metadata from within VTK, and some utility programs for interrogating and converting DICOM files.

#### Conversion

- [dcm2niix](https://github.com/rordenlab/dcm2niix) - Convert neuroimaging data from the DICOM format to the [NIfTI](https://nifti.nimh.nih.gov/) format.
- [DicomToMesh](https://github.com/AOT-AG/DicomToMesh) - A command line tool to transform a DICOM volume into a 3d surface mesh (_obj_, _stl_ or _ply_). Several mesh processing routines can be enabled, such as mesh reduction, smoothing or cleaning.
- [wsi-to-dicom-converter](https://github.com/GoogleCloudPlatform/wsi-to-dicom-converter) - Convert whole slide images (WSIs) to DICOM.

#### Other

- [DICOMautomaton](https://github.com/hdclark/DICOMautomaton) - A multipurpose tool for analyzing medical physics data with a focus on automation.
- [dovo](https://github.com/DraconPern/dovo) - Cross-platform software for importing DICOM CD/files and sending to PACS.

### Go

- [dicom](https://github.com/suyashkumar/dicom) - High performance Golang DICOM parser.

### Java

#### General

- [dcm4che](https://github.com/dcm4che/dcm4che) - A collection of open source applications and utilities for the healthcare enterprise.
- [Dicoogle](https://github.com/bioinformatics-ua/dicoogle) - An extensible, platform-independent and open-source PACS archive software that replaces the traditional centralized database with a more agile indexing and retrieval mechanism.
- [healthcare-dicom-dicomweb-adapter](https://github.com/GoogleCloudPlatform/healthcare-dicom-dicomweb-adapter) - A set of components that translate between traditional DICOM DIMSE protocols (e.g., C-STORE) and the RESTful DICOMWeb protocols (e.g., STOW-RS).

#### Visualization

- [Weasis](https://github.com/nroduit/Weasis) - A multipurpose standalone and web-based DICOM viewer with a highly modular architecture.

### JavaScript

#### General

- [cornerstoneWADOImageLoader](https://tinyurl.com/bcdb4bxa) - A [cornerstone.js](https://github.com/cornerstonejs/) Image Loader for DICOM P10 instances over HTTP (WADO-URI) or DICOMWeb (WADO-RS). This can be used to integrate cornerstone with WADO-URI servers, DICOMWeb servers or any other HTTP based server that returns DICOM P10 instances (e.g., Orthanc or custom servers).
- [Daikon](https://github.com/rii-mango/Daikon) - A pure JavaScript DICOM reader.
- [dcmjs](https://github.com/dcmjs-org/dcmjs) - JavaScript implementation of DICOM manipulation. This code is an outgrowth of several efforts to implement web applications for medical imaging.
- [dicomParser](https://tinyurl.com/mr39unuk) - Cornerstone.js' lightweight library for parsing DICOM P10 byte streams, as well as raw (not encapsulated in part 10) byte streams, in modern HTML5 based web browsers (IE10+), Node.js and Meteor.
- [dicomweb-client](https://github.com/dcmjs-org/dicomweb-client) - JavaScript client implementation of DICOMWeb.
- [dicomweb-pacs](https://github.com/knopkem/dicomweb-pacs) - Easy to use DICOMWeb enabled PACS with DIMSE services based on sqlite database.
- [dicomweb-server](https://github.com/dcmjs-org/dicomweb-server) - Lightweight DICOMWeb Server with CouchDB.
- [dcmjs-dimse](https://github.com/PantelisGeorgiadis/dcmjs-dimse) - DICOM DIMSE implementation for Node.js using the dcmjs library.

#### Visualization

- [bluelight](https://github.com/cylab-tw/bluelight) - Browser-based medical image viewer primarily maintained by the [Imaging Informatics Labs](https://cylab.dicom.tw/). It is a pure single-page application (SPA), lightweight, and using only JavaScript and HTML5 technologies to easily deploy it on any HTTP server.
- [cornerstone](https://tinyurl.com/2p85awt3) - A complete web based medical imaging platform. This repository contains the [cornerstone.js](https://github.com/cornerstonejs) "Core" component which is a lightweight JavaScript library for displaying medical images in modern web browsers that support the HTML5 canvas element.
- [dicom.ts](https://github.com/wearemothership/dicom.ts) - A small, superfast JS DICOM renderer.
- [dicom-microscopy-viewer](https://github.com/ImagingDataCommons/dicom-microscopy-viewer) - Vanilla JS library for web-based visualization of DICOM VL Whole Slide Microscopy Image datasets and derived information.
- [dicomviewer](https://github.com/ayselafsar/dicomviewer) - A DICOM viewer which uses the [cornerstone.js](https://github.com/cornerstonejs) library to display DICOM files in Nextcloud.
- [dicomViewerLib](https://github.com/fourctv/dicomViewerLib) - An Angular 9+ DICOMWeb viewer component, based on the cornerstone.js project.
- [DWV](https://github.com/ivmartel/dwv) - DICOM Web Viewer (DWV) is an open source zero footprint medical image viewer library. It uses only JavaScript and HTML5 technologies, meaning that it can be run on any platform that provides a modern browser (laptop, tablet, phone and even modern TVs).
- [dwv-react](https://github.com/ivmartel/dwv-react) - Medical viewer using DWV and [React](https://react.dev/).
- [U Dicom Viewer](https://github.com/webnamics/u-dicom-viewer) - A simple but functional DICOM viewer for any device with a web browser. Allows opening and viewing 2D medical images in a wide variety of DICOM formats.
- [Viewers](https://github.com/OHIF/Viewers) - A zero-footprint medical image viewer provided by the [Open Health Imaging Foundation (OHIF)](https://ohif.org/). It is a configurable and extensible progressive web application with out-of-the-box support for image archives which support DICOMWeb.
- [dcmjs-imaging](https://github.com/PantelisGeorgiadis/dcmjs-imaging) - DICOM image and overlay rendering pipeline for Node.js and browser using the dcmjs library.
- [dcmjs-ecg](https://github.com/PantelisGeorgiadis/dcmjs-ecg) - DICOM electrocardiography (ECG) rendering for Node.js and browser using dcmjs.

#### Other

- [dicomweb-proxy](https://github.com/knopkem/dicomweb-proxy) - Translates between DICOMWeb and traditional DICOM DIMSE services.

### MATLAB

#### Conversion

- [dicm2nii](https://github.com/xiangruili/dicm2nii) - Convert DICOM into NIfTI. It can also convert PAR/XML/REC, HEAD/BRIK, MGZ and BrainVoyager files into NIfTI.

### Python

#### General

- [dicompyler](https://github.com/dicompyler/) - An extensible open source radiation therapy research platform based on the DICOM standard. It also functions as a cross-platform DICOM RT viewer.
- [dicomweb-client](https://github.com/ImagingDataCommons/dicomweb-client) - Provides client interfaces for DICOMWeb RESTful services QIDO-RS, WADO-RS and STOW-RS to search, retrieve and store DICOM objects over the web, respectively.
- [highdicom](https://github.com/ImagingDataCommons/highdicom) - Provides high-level DICOM abstractions for the Python programming language to facilitate the creation and handling of DICOM objects for image-derived information, including image annotations, and image analysis results.
- [MedPy](https://github.com/loli/medpy) - An image processing library and collection of scripts targeted towards medical (i.e. high dimensional) image processing.
- [pydicom](https://github.com/pydicom/pydicom) - A pure Python package for working with DICOM files. It lets you read, modify and write DICOM data in an easy "pythonic" way.
- [pynetdicom](https://github.com/pydicom/pynetdicom) - A pure Python 3.7+ package that implements the DICOM networking protocol. Working with _pydicom_, it allows the easy creation of DICOM Service Class Users (SCUs) and Service Class Providers (SCPs).

#### Conversion

- [bidskit](https://github.com/jmtyszka/bidskit) - CLI for converting a directory of DICOM files into a [BIDS](https://bids.neuroimaging.io/)-compliant dataset.
- [dcmstack](https://github.com/moloney/dcmstack) - DICOM to NIfTI conversion with the added ability to extract and summarize metadata from the source files.
- [dicom2nifti](https://github.com/icometrix/dicom2nifti) - Convert MR and CT-derived DICOM files to NIfTI.
- [dicom2stl](https://github.com/dave3d/dicom2stl) - Convert a DICOM series to an [STL](<https://en.wikipedia.org/wiki/STL_(file_format)>) surface mesh.
- [Dicomifier](https://github.com/lamyj/dicomifier) - A set of tools to convert Bruker data to DICOM files, and DICOM files to NIfTI.
- [heudiconv](https://github.com/nipy/heudiconv) - A flexible DICOM converter for organizing brain imaging data into structured directory layouts.

#### Anonymization

- [deid](https://github.com/pydicom/deid) - Best effort anonymization for medical images in Python.
- [DICAT](https://github.com/aces/DICAT) - A simple graphical tool that facilitates DICOM de-identification directly on a local workstation.
- [dicom-anonymizer](https://github.com/KitwareMedical/dicom-anonymizer) - A tool for anonymizing DICOM files according to the DICOM standard.

#### Sorting

- [dicomsort](https://github.com/pieper/dicomsort) - Given DICOM files in a random folder structure, this program copies all into a user-defined folder hierarchy, creating folders as necessary and changing DICOM file names to be more meaningful.

#### Visualization

- [dicom-ecg-plot](https://github.com/marcodebe/dicom-ecg-plot) - Plot ECG data from DICOM ([demo](https://ecg.galliera.it/)).
- [OnkoDICOM](https://github.com/didymo/OnkoDICOM) - DICOM-RT viewer with enhanced capabilities that make it useful for research in the field of Radiation Oncology.
- [MRIcroGL](https://github.com/rordenlab/MRIcroGL) - A cross-platform tool for viewing DICOM and NIfTI format images. It provides a drag-and-drop user interface as well as a scripting language.

#### Other

- [dcmrtstruct2nii](https://github.com/Sikerdebaard/dcmrtstruct2nii) - DICOM RT-Struct to nii-mask. This is a naïve approach to rasterizing rt-struct to masks in the NIfTI format.
- [dicom-numpy](https://github.com/innolitics/dicom-numpy) - A set of utilities for extracting data contained in DICOM files into Numpy ndarrays.
- [dicom-standard](https://github.com/innolitics/dicom-standard) - Parses the web version of the DICOM Standard into human and machine-friendly JSON files.

### Rust

- [DICOM-rs](https://github.com/Enet4/dicom-rs) - A pure Rust implementation of the DICOM standard, allowing users to work with DICOM objects and interact with DICOM applications, while aiming to be fast, safe, and intuitive to use.

### Other/Combination

#### Machine Learning

- [mercure](https://github.com/mercure-imaging/mercure) - A flexible DICOM routing and processing solution with user-friendly web interface and extensive monitoring functions.
- [Niffler](https://github.com/Emory-HITI/Niffler) - A lightweight framework to facilitate executing machine learning pipelines and processing workflows on DICOM images and metadata.

#### Validation

- [DVTk](https://github.com/dvtk-org/DVTk) - Testing, validating and diagnosing DICOM communication in medical environments.

#### Visualization

- [AlizaMS](https://github.com/AlizaMedicalImaging/AlizaMS) - DICOM viewer.

#### Image Computing Platforms

- [3D Slicer](https://slicer.org) - Free and open source workstation software with tools for many clinical specialies and DICOM datatypes. Supports visualization, registration, segmentation, time series analysis and much more.

## Contribute

Contributions welcome! Read the [contribution guidelines](contributing.md) first.
