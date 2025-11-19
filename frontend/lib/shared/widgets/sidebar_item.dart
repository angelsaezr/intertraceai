import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

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
    return InkWell(
      onTap: () => context.go(route),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 17, vertical: 12),
        child: Row(
          children: [
            Icon(icon, color: Colors.white),

            if (!collapsed) ...[
              const SizedBox(width: 10),

              Expanded(
                child: Text(
                  label,
                  style: const TextStyle(color: Colors.white),
                  overflow: TextOverflow.ellipsis,
                  maxLines: 1,
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
