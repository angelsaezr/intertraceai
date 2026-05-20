class ChatMessage {
  final String text;
  final bool isUser;
  final bool isLoading;
  final List<String> sources; 

  ChatMessage({
    required this.text,
    required this.isUser,
    this.isLoading = false,
    this.sources = const [],
  });
}
