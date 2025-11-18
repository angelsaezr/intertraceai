import 'package:flutter/material.dart';
import 'package:frontend/example.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      themeMode: ThemeMode.dark,
      darkTheme: ThemeData.dark(),
      home: Scaffold(
        appBar: AppBar(
          title: Text("InterTraceAI"),
          backgroundColor: Colors.blue,
          leading: Image.asset("assets/images/icon.png"),
        ),
        body: Example(),
      ),
    );
  }
}
