import 'dart:convert';
import 'package:http/http.dart' as http;
import '../model/doc_item.dart';

class DocsRepository {
  final String baseUrl;
  DocsRepository({required this.baseUrl});

  Future<List<DocItem>> fetchDocuments() async {
    final res = await http.get(Uri.parse("$baseUrl/documents"));

    if (res.statusCode != 200) {
      throw Exception("Error ${res.statusCode}: ${res.body}");
    }

    final decoded = jsonDecode(res.body);
    if (decoded is! List) {
      throw Exception("Unexpected response: ${res.body}");
    }

    return decoded
        .whereType<Map<String, dynamic>>()
        .map(DocItem.fromJson)
        .toList();
  }
}
