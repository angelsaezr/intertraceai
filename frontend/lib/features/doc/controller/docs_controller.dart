import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../model/doc_item.dart';
import '../repository/docs_repository.dart';

class DocsState {
  final bool loading;
  final String? error;
  final List<DocItem> docs;

  const DocsState({
    required this.loading,
    required this.error,
    required this.docs,
  });

  factory DocsState.initial() => const DocsState(
        loading: false,
        error: null,
        docs: [],
      );

  DocsState copyWith({
    bool? loading,
    String? error,
    List<DocItem>? docs,
  }) {
    return DocsState(
      loading: loading ?? this.loading,
      error: error,
      docs: docs ?? this.docs,
    );
  }
}

final docsRepositoryProvider = Provider<DocsRepository>((ref) {
  return DocsRepository(baseUrl: "http://127.0.0.1:8000");
});

class DocsController extends Notifier<DocsState> {
  late final DocsRepository _repo;

  @override
  DocsState build() {
    _repo = ref.read(docsRepositoryProvider);
    // auto-load al entrar
    _load();
    return DocsState.initial();
  }

  Future<void> refresh() => _load();

  Future<void> _load() async {
    state = state.copyWith(loading: true, error: null);

    try {
      final docs = await _repo.fetchDocuments();
      // opcional: ordenar por fecha
      docs.sort((a, b) {
        final ad = a.createdAt ?? DateTime.fromMillisecondsSinceEpoch(0);
        final bd = b.createdAt ?? DateTime.fromMillisecondsSinceEpoch(0);
        return bd.compareTo(ad);
      });

      state = state.copyWith(loading: false, docs: docs, error: null);
    } catch (e) {
      state = state.copyWith(loading: false, error: e.toString());
    }
  }
}

final docsProvider = NotifierProvider<DocsController, DocsState>(
  DocsController.new,
);
