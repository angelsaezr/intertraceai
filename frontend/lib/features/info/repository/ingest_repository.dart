import 'dart:convert';
import 'package:http/http.dart' as http;

class IngestRepository {
  final String baseUrl;
  IngestRepository({required this.baseUrl});

  Future<Map<String, dynamic>> resetAndIngest() async {
    final res = await http.post(Uri.parse("$baseUrl/ingest/reset"));

    if (res.statusCode != 200) {
      throw Exception("Error ${res.statusCode}: ${res.body}");
    }
    return jsonDecode(res.body) as Map<String, dynamic>;
  }
}