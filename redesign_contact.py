import os
import re

filename = "contact.html"
with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

new_main = """<main class="w-full pt-20 bg-surface min-h-[calc(100vh-80px)] flex flex-col items-center py-10">
    <div class="w-full max-w-4xl mx-auto px-4 flex-1 flex flex-col h-[70vh]">
        <!-- Tiêu đề trang -->
        <div class="text-center mb-8">
            <h1 class="text-3xl md:text-4xl font-bold text-on-surface mb-2">Hỗ trợ trực tuyến</h1>
            <p class="text-on-surface-variant">Đội ngũ chuyên gia Apple của chúng tôi luôn sẵn sàng giải đáp mọi thắc mắc của bạn.</p>
        </div>

        <!-- Khung Chat -->
        <div class="flex-1 bg-white rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-gray-100 flex flex-col overflow-hidden">
            
            <!-- Chat Header -->
            <div class="flex items-center gap-4 px-6 py-4 bg-gray-50 border-b border-gray-100">
                <div class="relative">
                    <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuDAjm4Z8NMGCwxjt_rxm_h4sTMNZm20HkezoeVXopQmQsHrSKLbQ5p48cVWkL0peNcq9_3ozdHR4Sg83lRUIitvSIZgnsffAiolrpATr7XPOnetiAHdUnkxwEnWZUesa0LQjIhkSMaK0S0ujul1lmvydBsrnCgy4stDjCPYGA5s19jqVn-z5tPlydkacPZeJe5-A0zv2NxTqJrw_9q103Z38C3707vVfb4f1nXB2-0" alt="Admin" class="w-12 h-12 rounded-full object-cover">
                    <span class="absolute bottom-0 right-0 w-3.5 h-3.5 bg-green-500 border-2 border-white rounded-full"></span>
                </div>
                <div>
                    <h3 class="font-semibold text-gray-900">iStore Support Team</h3>
                    <p class="text-sm text-green-600 font-medium">Đang hoạt động</p>
                </div>
            </div>

            <!-- Chat Messages -->
            <div class="flex-1 p-6 overflow-y-auto bg-white flex flex-col gap-6" id="chat-messages">
                <!-- Message từ Admin -->
                <div class="flex items-end gap-3 max-w-[80%]">
                    <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuDAjm4Z8NMGCwxjt_rxm_h4sTMNZm20HkezoeVXopQmQsHrSKLbQ5p48cVWkL0peNcq9_3ozdHR4Sg83lRUIitvSIZgnsffAiolrpATr7XPOnetiAHdUnkxwEnWZUesa0LQjIhkSMaK0S0ujul1lmvydBsrnCgy4stDjCPYGA5s19jqVn-z5tPlydkacPZeJe5-A0zv2NxTqJrw_9q103Z38C3707vVfb4f1nXB2-0" alt="Admin" class="w-8 h-8 rounded-full object-cover">
                    <div class="bg-gray-100 text-gray-800 px-5 py-3 rounded-2xl rounded-bl-none text-[15px] leading-relaxed">
                        Xin chào! 👋 Cảm ơn bạn đã liên hệ với iStore VN/A. Tôi có thể giúp gì cho bạn hôm nay?
                    </div>
                </div>

                <!-- Message từ Admin (Gợi ý) -->
                <div class="flex items-end gap-3 max-w-[80%] mt-2">
                    <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuDAjm4Z8NMGCwxjt_rxm_h4sTMNZm20HkezoeVXopQmQsHrSKLbQ5p48cVWkL0peNcq9_3ozdHR4Sg83lRUIitvSIZgnsffAiolrpATr7XPOnetiAHdUnkxwEnWZUesa0LQjIhkSMaK0S0ujul1lmvydBsrnCgy4stDjCPYGA5s19jqVn-z5tPlydkacPZeJe5-A0zv2NxTqJrw_9q103Z38C3707vVfb4f1nXB2-0" alt="Admin" class="w-8 h-8 rounded-full object-cover opacity-0">
                    <div class="flex flex-col gap-2">
                        <p class="text-sm text-gray-500 ml-2">Các chủ đề phổ biến:</p>
                        <div class="flex flex-wrap gap-2">
                            <span class="px-4 py-2 bg-white border border-gray-200 text-primary hover:bg-gray-50 rounded-full text-sm cursor-pointer transition-colors shadow-sm">Chính sách bảo hành</span>
                            <span class="px-4 py-2 bg-white border border-gray-200 text-primary hover:bg-gray-50 rounded-full text-sm cursor-pointer transition-colors shadow-sm">Thu cũ đổi mới</span>
                            <span class="px-4 py-2 bg-white border border-gray-200 text-primary hover:bg-gray-50 rounded-full text-sm cursor-pointer transition-colors shadow-sm">Báo giá iPhone 16 Pro</span>
                        </div>
                    </div>
                </div>

                <!-- Message từ Người dùng -->
                <div class="flex items-end gap-3 max-w-[80%] self-end">
                    <div class="bg-primary text-white px-5 py-3 rounded-2xl rounded-br-none text-[15px] leading-relaxed shadow-sm">
                        Mình muốn hỏi về chính sách trả góp qua thẻ tín dụng.
                    </div>
                </div>
            </div>

            <!-- Chat Input -->
            <div class="p-4 bg-white border-t border-gray-100">
                <form class="flex items-center gap-3 relative bg-gray-50 p-2 rounded-full border border-gray-200 focus-within:border-primary/50 focus-within:ring-2 focus-within:ring-primary/20 transition-all">
                    <button type="button" class="p-2 text-gray-400 hover:text-primary transition-colors rounded-full hover:bg-gray-100 flex items-center justify-center">
                        <span class="material-symbols-outlined text-[22px]">attach_file</span>
                    </button>
                    <input type="text" placeholder="Nhập tin nhắn của bạn..." class="flex-1 bg-transparent border-none outline-none text-[15px] text-gray-800 placeholder:text-gray-400 px-2 py-1">
                    <button type="submit" class="bg-primary text-white w-10 h-10 rounded-full flex items-center justify-center hover:bg-primary/90 transition-transform active:scale-95 flex-shrink-0 shadow-md">
                        <span class="material-symbols-outlined text-[20px] ml-0.5">send</span>
                    </button>
                </form>
            </div>

        </div>
    </div>
</main>"""

content = re.sub(r'<main.*?</main>', new_main, content, flags=re.DOTALL)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated contact.html design.")
