import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';
import '../utils/api.dart';

class SummaryController {
  File? selectedFile;
  bool isLoading = false;
  String summary = '';

  Future<void> pickPDF() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf'],
    );

    if (result != null) {
      selectedFile = File(result.files.single.path!);
    }
  }

  Future<void> summarize(BuildContext context) async {
    if (selectedFile == null) return;

    isLoading = true;
    summary = await Api.uploadPDF(selectedFile!);
    isLoading = false;

    Navigator.pushNamed(context, '/summary', arguments: summary);
  }
}
