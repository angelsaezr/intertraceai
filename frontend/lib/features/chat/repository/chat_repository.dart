import 'package:http/http.dart' as http;
import 'dart:convert';

class ChatRepository {
  final String baseUrl;

  ChatRepository({required this.baseUrl});

  Future<String> sendQuery(String message) async {
    final response = await http.post(
      Uri.parse("$baseUrl/query"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"question": message}),
    );

    if (response.statusCode != 200) {
      throw Exception("Error: ${response.body}");
    }

    return jsonDecode(response.body)["answer"];
  }
}
