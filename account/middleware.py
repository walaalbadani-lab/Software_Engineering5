import time

class SimpleLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # الكود الذي يتم تنفيذه قبل وصول الطلب للـ View
        start_time = time.time()

        response = self.get_response(request)

        # الكود الذي يتم تنفيذه بعد معالجة الـ View وقبل إرسال الرد
        duration = time.time() - start_time
        print(f"[MIDDLEWARE LOG] المسار: {request.path} | زمن التنفيذ: {duration:.4f} ثانية")

        return response