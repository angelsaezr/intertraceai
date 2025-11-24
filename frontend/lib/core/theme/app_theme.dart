import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData dark() {
    final base = ThemeData.dark();

    return base.copyWith(
      textTheme: base.textTheme.apply(fontFamily: "StackSans"),

      filledButtonTheme: FilledButtonThemeData(
        style: ButtonStyle(
          foregroundColor: WidgetStateProperty.all(Colors.white),
          textStyle: WidgetStateProperty.all(
            const TextStyle(fontFamily: "StackSans"),
          ),
        ),
      ),

      appBarTheme: const AppBarTheme(
        titleTextStyle: TextStyle(fontFamily: "StackSans", fontSize: 18),
      ),
    );
  }
}
