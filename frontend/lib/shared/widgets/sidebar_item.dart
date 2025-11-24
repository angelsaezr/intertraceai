import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:intertraceai/core/theme/app_colors.dart';

class SidebarItem extends StatelessWidget {
  final IconData icon;
  final String label;
  final String route;
  final bool collapsed;

  const SidebarItem({
    super.key,
    required this.icon,
    required this.label,
    required this.route,
    required this.collapsed,
  });

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: label,
      waitDuration: Duration(milliseconds: 300),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: () => context.go(route),
          borderRadius: BorderRadius.circular(10),
          hoverColor: Color.fromRGBO(231, 231, 231, 0.336),
          splashColor: AppColors.primary.withValues(),
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: collapsed
                ? Center(child: Icon(icon, size: 24))
                : Row(
                    children: [
                      Icon(icon, size: 24),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          label,
                          overflow: TextOverflow.ellipsis,
                          maxLines: 1,
                        ),
                      ),
                    ],
                  ),
          ),
        ),
      ),
    );
  }
}
