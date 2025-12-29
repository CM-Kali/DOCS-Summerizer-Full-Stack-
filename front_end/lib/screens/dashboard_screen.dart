import 'package:flutter/material.dart';
import '../controllers/summary_controller.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  final controller = SummaryController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Upload Document')),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            ElevatedButton(
              onPressed: () async {
                await controller.pickPDF();
                setState(() {});
              },
              child: const Text('Select PDF'),
            ),
            const SizedBox(height: 10),
            Text(
              controller.selectedFile?.path.split('/').last ?? 'No file selected',
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () async {
                setState(() => controller.isLoading = true);
                await controller.summarize(context);
                setState(() => controller.isLoading = false);
              },
              child: const Text('Summarize'),
            ),
            const SizedBox(height: 20),
            if (controller.isLoading)
              const CircularProgressIndicator(),
          ],
        ),
      ),
    );
  }
}
