import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../repository/ingest_repository.dart';

class IngestState {
  final bool loading;
  final String? result;

  const IngestState({required this.loading, required this.result});

  factory IngestState.initial() => const IngestState(loading: false, result: null);

  IngestState copyWith({bool? loading, String? result}) {
    return IngestState(
      loading: loading ?? this.loading,
      result: result,
    );
  }
}

final ingestRepositoryProvider = Provider<IngestRepository>((ref) {
  return IngestRepository(baseUrl: "http://127.0.0.1:8000");
});

class IngestController extends Notifier<IngestState> {
  late final IngestRepository _repo;

  @override
  IngestState build() {
    _repo = ref.read(ingestRepositoryProvider);
    return IngestState.initial();
  }

  Future<void> resetAndIngest() async {
    state = state.copyWith(loading: true, result: null);

    try {
      final data = await _repo.resetAndIngest();

      state = state.copyWith(
        loading: false,
        result: "${data["message"]}"
      );
    } catch (e) {
      state = state.copyWith(loading: false, result: "Ingest failed: $e");
    }
  }
}

final ingestProvider = NotifierProvider<IngestController, IngestState>(
  IngestController.new,
);
