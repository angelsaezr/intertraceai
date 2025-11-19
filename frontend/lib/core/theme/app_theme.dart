import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData dark() {
    final base = ThemeData.dark();

    return base.copyWith(
      textTheme: base.textTheme.apply(
        fontFamily: "StackSans",
      ),
      appBarTheme: const AppBarTheme(
        titleTextStyle: TextStyle(
          fontFamily: "StackSans",
          fontWeight: FontWeight.w600,
          fontSize: 18,
        ),
      ),
      primaryTextTheme: base.primaryTextTheme.apply(
        fontFamily: "StackSans",
      ),
    );
  }
}
