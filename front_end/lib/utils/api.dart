import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class Api {
  static const String baseUrl = "http://10.0.2.2:8000/summarize/";

  static Future<String> uploadPDF(File file) async {
    var request = http.MultipartRequest('POST', Uri.parse(baseUrl));
    request.files.add(await http.MultipartFile.fromPath('file', file.path));

    var response = await request.send();
    var responseData = await response.stream.bytesToString();

    if (response.statusCode == 200) {
      final json = jsonDecode(responseData);
      return json['summary'];
    } else {
      return "Error occurred";
    }
  }
}
