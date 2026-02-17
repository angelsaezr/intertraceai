class DocItem {
  final int? id;
  final String name;
  final String path;
  final DateTime? createdAt;

  DocItem({
    required this.id,
    required this.name,
    required this.path,
    required this.createdAt,
  });

  factory DocItem.fromJson(Map<String, dynamic> json) {
    return DocItem(
      id: json["id"] as int?,
      name: (json["name"] ?? "") as String,
      path: (json["path"] ?? "") as String,
      createdAt: json["created_at"] != null
          ? DateTime.tryParse(json["created_at"] as String)
          : null,
    );
  }
}
