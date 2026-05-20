import 'package:http/http.dart' as http;
import 'dart:convert';

class ChatRepository {
  final String baseUrl;

  ChatRepository({required this.baseUrl});

  Future<Map<String, dynamic>> sendQuery(String message) async {
    final response = await http.post(
      Uri.parse("$baseUrl/query"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"question": message}),
    );

    if (response.statusCode != 200) {
      throw Exception("Error: ${response.body}");
    }

    final body = jsonDecode(response.body);
    return {
      "answer": body["answer"] as String,
      "sources": (body["sources"] as List<dynamic>).cast<String>(),
    };
  }
}
