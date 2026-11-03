from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import sys

F = "/System/Library/Fonts/Supplemental/"
pdfmetrics.registerFont(TTFont("A", F + "Arial.ttf"))
pdfmetrics.registerFont(TTFont("AB", F + "Arial Bold.ttf"))
pdfmetrics.registerFont(TTFont("AI", F + "Arial Italic.ttf"))
pdfmetrics.registerFont(TTFont("ABI", F + "Arial Bold Italic.ttf"))
pdfmetrics.registerFontFamily("A", normal="A", bold="AB", italic="AI", boldItalic="ABI")

NAVY = colors.HexColor("#1F3A5F")
ACCENT = colors.HexColor("#C8963E")
LIGHT = colors.HexColor("#F3F0E8")
GRID = colors.HexColor("#D5CFC2")

body = ParagraphStyle("body", fontName="A", fontSize=10, leading=14.5, spaceAfter=4)
small = ParagraphStyle("small", parent=body, fontSize=9, leading=12.5, spaceAfter=0)
h1 = ParagraphStyle("h1", fontName="AB", fontSize=15, leading=19, textColor=NAVY, spaceBefore=8, spaceAfter=6)
h2 = ParagraphStyle("h2", fontName="AB", fontSize=11.5, leading=15, textColor=NAVY, spaceBefore=8, spaceAfter=3)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=12, bulletIndent=2, spaceAfter=2)
title = ParagraphStyle("title", fontName="AB", fontSize=24, leading=30, textColor=NAVY, spaceAfter=4)
subtitle = ParagraphStyle("subtitle", fontName="A", fontSize=12.5, leading=17, textColor=colors.HexColor("#555555"), spaceAfter=10)
th = ParagraphStyle("th", parent=small, fontName="AB", textColor=colors.white)
note = ParagraphStyle("note", parent=body, fontName="AI", textColor=colors.HexColor("#444444"))


def P(t, s=body):
    return Paragraph(t, s)


def bullets(items):
    return [Paragraph(i, bullet, bulletText="•") for i in items]


def table(rows, widths, header=True):
    data = [[P(c, th if (header and r == 0) else small) for c in row] for r, row in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [
        ("GRID", (0, 0), (-1, -1), 0.5, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), NAVY))
    for r in range(1 if header else 0, len(rows)):
        if r % 2 == 0:
            st.append(("BACKGROUND", (0, r), (-1, r), LIGHT))
    t.setStyle(TableStyle(st))
    return t


def box(content, color=LIGHT):
    t = Table([[content]], colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("LINEBEFORE", (0, 0), (0, -1), 3, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def footer(c, d):
    c.saveState()
    c.setFont("A", 8)
    c.setFillColor(colors.HexColor("#888888"))
    c.drawString(20 * mm, 12 * mm, "Tài liệu huấn luyện FreeShow nâng cao")
    c.drawRightString(190 * mm, 12 * mm, f"Trang {d.page}")
    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.8)
    c.line(20 * mm, 15 * mm, 190 * mm, 15 * mm)
    c.restoreState()


s = []

# ---------- Trang 1 ----------
s += [
    P("Tài liệu huấn luyện FreeShow nâng cao", title),
    P("Dành cho ban kỹ thuật, trình chiếu và livestream đã hoàn thành khóa cơ bản", subtitle),
]
s.append(box(P(
    "Khóa cơ bản giúp một người vận hành trọn một buổi thờ phượng. Khóa nâng cao hướng tới việc "
    "<b>xây dựng hệ thống</b>: nhiều màn hình với nội dung khác nhau, livestream chất lượng, tự động hóa "
    "thao tác lặp lại, phân quyền cho đội ngũ, đồng bộ dữ liệu giữa nhiều máy và nhiều chi hội.")))
s.append(Spacer(1, 8))

s.append(P("1. Điều kiện tham gia", h1))
s += bullets([
    "Đã hoàn thành khóa cơ bản hoặc đã vận hành FreeShow ít nhất 1–2 tháng.",
    "Thành thạo Project, Show, Layout, Style, Kinh Thánh, Overlay, Stage và Remote.",
    "Có hiểu biết cơ bản về mạng LAN/Wi-Fi, địa chỉ IP, cáp HDMI/SDI và phần mềm OBS (cho phần livestream).",
])

s.append(P("2. Mục tiêu", h1))
s += bullets([
    "Thiết kế sơ đồ trình chiếu cho Hội Thánh: máy chiếu chính, TV sảnh, màn hình bục, livestream, phòng thiếu nhi.",
    "Đưa hình ảnh FreeShow vào hệ thống video bằng <b>NDI, OMT, Blackmagic (SDI), WebRTC hoặc RTMP</b>.",
    "Tự động hóa bằng <b>Actions, Triggers, MIDI, Variables, Timeline</b> và điều khiển qua <b>API</b> (Companion, Stream Deck).",
    "Quản lý đội ngũ bằng <b>Profiles</b> (phân quyền), <b>Cloud sync</b> và kế hoạch sao lưu.",
    "Ứng dụng <b>phụ đề trực tiếp</b> và <b>AI nhận dạng giọng nói</b> một cách có trách nhiệm.",
])

s.append(P("3. Chương trình", h1))
s.append(table([
    ["Buổi", "Chủ đề", "Thời lượng"],
    ["A", "Hệ thống nhiều Output, Stage tùy chỉnh, xuất hình qua mạng và livestream", "150 phút"],
    ["B", "Tự động hóa: Actions, Triggers, MIDI, API, Variables, Timeline, Timecode", "150 phút"],
    ["C", "Đội ngũ & dữ liệu: Profiles, Cloud sync, nguồn nội dung, phụ đề, AI", "120 phút"],
    ["D", "Thiết kế hệ thống cho Hội Thánh mình, diễn tập và đánh giá", "150 phút"],
], [18 * mm, 125 * mm, 27 * mm]))
s.append(Spacer(1, 6))
s.append(P("Gợi ý: học trên chính hệ thống của nhà thờ. Mỗi nhóm 2–3 người cần 1 máy chạy FreeShow, 1 màn hình phụ, 1 điện thoại hoặc máy tính bảng, và (nếu có) 1 máy chạy OBS cùng mạng LAN.", note))

s.append(PageBreak())

# ---------- Trang 2 ----------
s.append(P("4. Buổi A — Hệ thống Output và livestream", h1))
s.append(P("4.1 Nhiều Output, mỗi màn hình một nội dung", h2))
s += bullets([
    "Vào <b>Cài đặt → Outputs</b> để tạo nhiều Output. Mỗi Output gán cho một màn hình vật lý hoặc một ngõ ra qua mạng.",
    "Mỗi Output có <b>Style riêng</b>: máy chiếu chính dùng chữ lớn và nền video; Output livestream dùng chữ nhỏ ở 1/3 dưới với nền trong suốt; TV sảnh chỉ hiện thông báo.",
    "Có thể bật/tắt từng Output và chọn Output nào nhận slide, nền hoặc overlay.",
    "Hiệu chỉnh vị trí, kích thước và tỉ lệ khung hình (16:9, 4:3) cho từng màn hình để khớp với máy chiếu cũ.",
])
s.append(P("4.2 Màn hình bục tùy chỉnh (Stage layouts)", h2))
s += bullets([
    "Tạo nhiều bố cục Stage cho từng đối tượng: <b>ban hát</b> (slide hiện tại + kế tiếp + hợp âm), <b>người giảng</b> (đồng hồ, ghi chú, tin nhắn), <b>ban kỹ thuật</b> (giờ hiện tại, đếm ngược).",
    "Mỗi Stage mở trên thiết bị khác nhau qua trình duyệt (cổng 5511), có thể đặt mật khẩu.",
    "Dùng tin nhắn trên Stage để nhắc người giảng (ví dụ “còn 5 phút”) mà hội chúng không thấy.",
])
s.append(P("4.3 Xuất hình qua mạng và phần cứng video", h2))
s.append(table([
    ["Ngõ ra", "Dùng khi", "Lưu ý"],
    ["NDI", "Đưa lời bài hát vào OBS, vMix hoặc bàn trộn hình trong cùng mạng LAN, có kênh alpha (nền trong suốt)", "Nên dùng mạng dây (Gigabit); OBS cần plugin NDI"],
    ["OMT", "Giao thức mã nguồn mở tương tự NDI, độ trễ thấp", "Kiểm tra phần mềm nhận có hỗ trợ OMT"],
    ["Blackmagic (SDI/HDMI)", "Hệ thống chuyên nghiệp dùng card DeckLink hoặc ATEM", "Cần card Blackmagic và driver Desktop Video"],
    ["WebRTC / trình duyệt", "Xem Output trên thiết bị bất kỳ qua trình duyệt (cổng 5513)", "Tiện nhưng độ trễ cao hơn NDI"],
    ["RTMP", "Phát thẳng lên YouTube/Facebook không cần OBS", "Cần FFmpeg; phù hợp nếu chỉ phát lời và slide"],
    ["Camera điện thoại", "Dùng điện thoại làm camera nguồn qua trình duyệt", "Cùng mạng Wi-Fi, nên cố định điện thoại"],
], [34 * mm, 80 * mm, 56 * mm]))
s.append(P("4.4 Mô hình livestream khuyến nghị", h2))
s += bullets([
    "FreeShow tạo một Output riêng cho livestream: <b>nền trong suốt</b>, chữ ở 1/3 dưới màn hình, có viền/bóng.",
    "Bật <b>NDI</b> cho Output đó. Trong OBS, thêm nguồn NDI đặt <b>trên</b> lớp camera, rồi phát lên Facebook/YouTube.",
    "Ghi hình (Recording) Output trực tiếp trong FreeShow để lưu trữ hoặc cắt clip mạng xã hội.",
    "Kiểm tra độ trễ giữa âm thanh và lời bài hát; nếu cần, chỉnh độ trễ trong OBS.",
])

s.append(PageBreak())

# ---------- Trang 3 ----------
s.append(P("5. Buổi B — Tự động hóa và điều khiển", h1))
s.append(P("5.1 Actions và Triggers", h2))
s += bullets([
    "<b>Action</b> là một chuỗi thao tác gói thành một nút bấm. Ví dụ “Bắt đầu buổi nhóm”: xóa tất cả → bật nền video → bật đồng hồ đếm ngược → phát nhạc nền.",
    "Gán Action cho <b>phím tắt</b>, <b>slide</b> (tự chạy khi vào slide), <b>Project</b> hoặc <b>lịch</b> (chạy theo giờ).",
    "<b>Triggers</b> gửi lệnh ra ngoài khi một slide được bật, ví dụ gọi HTTP tới bộ điều khiển đèn hoặc phần mềm khác.",
    "Dùng <b>Conditions</b> (điều kiện) để Action chỉ chạy khi thỏa điều kiện, ví dụ chỉ khi Output đang bật.",
])
s.append(P("5.2 MIDI, Stream Deck và bút trình chiếu", h2))
s += bullets([
    "Nhận tín hiệu <b>MIDI</b> từ bàn phím đàn, pad hoặc bàn trộn âm thanh để chuyển slide hoặc chạy Action. Ban nhạc có thể tự chuyển slide bằng pedal.",
    "Dùng <b>Bitfocus Companion</b> với <b>Stream Deck</b> để có bảng nút vật lý: bài kế tiếp, xóa chữ, bật logo, đổi nền.",
    "Bút trình chiếu gửi phím mũi tên/PageUp/PageDown; FreeShow nhận trực tiếp mà không cần cấu hình.",
])
s.append(P("5.3 API điều khiển từ xa", h2))
s.append(table([
    ["Giao thức", "Cổng mặc định", "Ứng dụng"],
    ["WebSocket", "5505", "Ứng dụng tùy chỉnh, Companion, bảng điều khiển web"],
    ["REST (HTTP)", "5506", "Gọi lệnh từ các hệ thống khác (đèn, tự động hóa nhà thờ)"],
    ["OSC", "5505", "Bàn trộn âm thanh, phần mềm sân khấu (QLab…)"],
], [35 * mm, 35 * mm, 100 * mm]))
s.append(Spacer(1, 3))
s.append(P("Bật API trong <b>Cài đặt → Connection</b>. Luôn đặt <b>mật khẩu</b> và chỉ mở API trong mạng nội bộ của nhà thờ.", note))
s.append(P("5.4 Variables và Dynamic values", h2))
s += bullets([
    "<b>Variables</b> (biến) có kiểu số, văn bản, bộ văn bản hoặc số ngẫu nhiên. Ví dụ biến “Người giảng” và “Chủ đề”: đổi một lần, mọi slide và overlay dùng biến đó tự cập nhật.",
    "<b>Dynamic values</b> chèn thông tin tự động vào slide: giờ hiện tại, tên bài hát, số slide, slide kế tiếp, giá trị đồng hồ, giá trị biến.",
    "Ứng dụng: lower third “Mục sư {tên} – {chủ đề}” dùng lại mỗi tuần mà không phải sửa overlay.",
])
s.append(P("5.5 Timeline, Timecode và Lịch", h2))
s += bullets([
    "<b>Timeline</b> ghi lại các thao tác theo thời gian (chuyển slide, xóa lớp…) để phát lại đúng nhịp, phù hợp cho tiết mục đặc biệt hoặc video có lời dựng sẵn.",
    "<b>Timecode (LTC/MTC)</b> đồng bộ FreeShow với phần mềm âm thanh/ánh sáng, dùng cho chương trình Giáng Sinh, Phục Sinh có nhạc nền cố định.",
    "<b>Lịch (Calendar)</b> đặt sự kiện lặp lại hằng ngày/tuần/tháng để tự mở Project hoặc chạy Action, ví dụ tự chạy slide thông báo 20 phút trước giờ nhóm.",
])

s.append(PageBreak())

# ---------- Trang 4 ----------
s.append(P("6. Buổi C — Đội ngũ, dữ liệu và công nghệ mới", h1))
s.append(P("6.1 Profiles — phân quyền người dùng", h2))
s += bullets([
    "Tạo nhiều <b>Profile</b> (vai trò) để giới hạn quyền điều khiển/chỉnh sửa từng phần của chương trình.",
    "Ví dụ: Profile “Người mới” chỉ được trình chiếu, không sửa bài hát hay Style; Profile “Quản trị” có toàn quyền.",
    "Giúp người mới tập sự an toàn, tránh vô tình xóa hoặc sửa thư viện chung.",
])
s.append(P("6.2 Đồng bộ và sao lưu", h2))
s.append(table([
    ["Cách làm", "Phù hợp", "Ghi chú"],
    ["Cloud sync (ChurchApps)", "Nhiều máy cùng Hội Thánh, nhiều chi hội dùng chung thư viện", "Chọn danh mục cần đồng bộ; kiểm tra trước khi xóa trên một máy"],
    ["Thư mục đồng bộ (Drive, OneDrive, Dropbox)", "Hội Thánh nhỏ, 2–3 máy", "Không mở cùng lúc trên hai máy để tránh xung đột"],
    ["Sao lưu định kỳ", "Mọi Hội Thánh", "Cài đặt → Sao lưu, mỗi tuần; giữ một bản ngoài máy (ổ USB, đám mây)"],
], [45 * mm, 65 * mm, 60 * mm]))
s.append(P("6.3 Nguồn nội dung bên ngoài", h2))
s += bullets([
    "Kết nối <b>Planning Center</b> hoặc <b>ChurchApps</b> để lấy chương trình buổi nhóm và bài hát đã lên kế hoạch.",
    "Nhập thiết kế từ <b>Canva</b> cho thông báo và hình nền đồng bộ với nhận diện của Hội Thánh.",
    "Thống nhất <b>quy ước đặt tên</b> và danh mục (Thánh ca số…, Tôn vinh, Thiếu nhi, Lễ đặc biệt) trước khi đồng bộ.",
])
s.append(P("6.4 Phụ đề trực tiếp (Captions)", h2))
s += bullets([
    "Nhận dạng lời giảng qua micro và hiển thị phụ đề trên màn hình; có thể <b>dịch</b> sang ngôn ngữ khác cho khách nước ngoài hoặc Hội Thánh song ngữ.",
    "Mở trang phụ đề bằng Google Chrome, cấp quyền micro; nên dùng micro sạch từ bàn trộn thay vì micro laptop.",
    "Giải thích với hội chúng rằng phụ đề tự động có thể sai, đặc biệt với tên riêng và từ Kinh Thánh.",
])
s.append(P("6.5 AI — nghe giọng nói và gợi ý thao tác", h2))
s += bullets([
    "Tính năng AI nghe micro, chuyển lời nói thành văn bản và <b>gợi ý thao tác</b>, ví dụ người giảng nói “Giăng 3:16” thì gợi ý chiếu câu đó.",
    "Có thể chạy <b>mô hình cục bộ</b> trên máy (dữ liệu không rời máy) hoặc liên kết với nhà cung cấp LLM (OpenAI, Anthropic, Google, Ollama) để hiểu ngữ cảnh tốt hơn.",
    "Chọn mức tự động: <b>luôn hỏi</b>, hoặc chỉ tự trình chiếu khi độ tin cậy cao. Khuyến nghị bắt đầu với “luôn hỏi”.",
])
s.append(box(P("<b>Lưu ý quyền riêng tư:</b> khi dùng nhà cung cấp đám mây, văn bản lời giảng được gửi lên máy chủ bên ngoài. "
               "Cần sự đồng ý của mục sư và ban chấp sự, và không dùng cho các buổi cầu nguyện, tư vấn hoặc nội dung nhạy cảm.")))

s.append(PageBreak())

# ---------- Trang 5 ----------
s.append(P("7. Buổi D — Thiết kế hệ thống cho Hội Thánh", h1))
s.append(P("7.1 Ba mô hình tham khảo", h2))
s.append(table([
    ["Quy mô", "Thiết bị", "Cấu hình FreeShow"],
    ["Nhỏ (dưới 80 người)", "1 laptop, 1 máy chiếu, 1 điện thoại", "1 Output; Remote trên điện thoại cho người giảng; Stage trên chính laptop hoặc máy tính bảng"],
    ["Vừa (80–300 người)", "1 máy bàn, máy chiếu + TV bục, router riêng, máy OBS", "2–3 Output (chính, bục, livestream NDI); Stage cho ban hát; Actions cho đầu/cuối buổi; Stream Deck"],
    ["Lớn / nhiều chi hội", "Máy chính + máy dự phòng, card Blackmagic, bàn trộn hình, mạng dây", "Nhiều Output (SDI/NDI); Profiles phân quyền; Cloud sync giữa các máy và chi hội; Timecode cho chương trình lớn"],
], [32 * mm, 58 * mm, 80 * mm]))
s.append(P("7.2 Checklist kỹ thuật", h2))
s.append(table([
    ["Hạng mục", "Kiểm tra"],
    ["Mạng", "Router riêng cho ban kỹ thuật; IP tĩnh cho máy FreeShow; mạng dây cho NDI; Wi-Fi riêng cho Remote/Stage"],
    ["Máy tính", "Tắt chế độ ngủ, cập nhật tự động và thông báo hệ thống trong giờ nhóm; ổ SSD; card đồ họa đủ mạnh cho video 1080p"],
    ["Dự phòng", "Máy thứ hai có cùng dữ liệu (Cloud sync); cáp HDMI dự phòng; Project xuất sẵn ra USB"],
    ["Bảo mật", "Mật khẩu cho Remote, Stage, API; không mở cổng ra Internet; Profile hạn chế cho người mới"],
    ["Cập nhật phần mềm", "Cập nhật FreeShow giữa tuần, không cập nhật sáng Chúa nhật; thử trước trên máy phụ"],
], [32 * mm, 138 * mm]))
s.append(P("7.3 Xử lý sự cố nâng cao", h2))
s.append(table([
    ["Hiện tượng", "Cách xử lý"],
    ["OBS không thấy nguồn NDI", "Kiểm tra cùng mạng/subnet, tường lửa cho phép FreeShow và OBS, đã cài plugin NDI; thử khởi động lại Output NDI"],
    ["Lời bài hát trên livestream bị nền đen", "Bật nền trong suốt cho Output livestream; trong OBS dùng nguồn NDI có alpha, không dùng chụp màn hình"],
    ["Companion/Stream Deck không điều khiển được", "Bật API trong Connection, đúng IP và cổng 5505/5506, đúng mật khẩu"],
    ["Hai máy đồng bộ bị mất/ghi đè bài hát", "Chỉ một máy chỉnh sửa tại một thời điểm; khôi phục từ bản sao lưu; kiểm tra danh mục đồng bộ"],
    ["MIDI không phản hồi", "Chọn đúng thiết bị MIDI vào trong Action; kiểm tra kênh và nốt/CC khớp với tín hiệu gửi"],
], [52 * mm, 118 * mm]))

s.append(PageBreak())

# ---------- Trang 6 ----------
s.append(P("8. Bài tập thực hành nâng cao", h1))
s.append(table([
    ["#", "Bài tập", "Tiêu chí đạt"],
    ["1", "Tạo 3 Output: máy chiếu chính, màn hình bục, livestream (nền trong suốt, chữ 1/3 dưới)", "Mỗi Output đúng Style, bật/tắt độc lập"],
    ["2", "Đưa Output livestream vào OBS qua NDI, đặt trên lớp camera", "Lời bài hát rõ, không nền đen, trễ chấp nhận được"],
    ["3", "Thiết kế 2 Stage layout: ban hát (hợp âm, slide kế) và người giảng (đồng hồ, tin nhắn)", "Mở được trên 2 thiết bị khác nhau"],
    ["4", "Tạo Action “Bắt đầu buổi nhóm” và “Kết thúc buổi nhóm”, gán phím tắt", "Một phím thực hiện đủ chuỗi thao tác"],
    ["5", "Tạo biến “Người giảng” và lower third dùng Dynamic value", "Đổi biến → overlay tự cập nhật"],
    ["6", "Điều khiển FreeShow bằng Stream Deck/Companion hoặc pedal MIDI", "Chuyển slide và xóa chữ từ thiết bị ngoài"],
    ["7", "Tạo Profile “Người mới” giới hạn quyền chỉnh sửa", "Người dùng Profile không sửa được thư viện"],
    ["8", "Thiết kế sơ đồ hệ thống cho Hội Thánh mình và trình bày trước lớp", "Có sơ đồ, danh sách thiết bị, phương án dự phòng"],
], [10 * mm, 102 * mm, 58 * mm]))

s.append(P("9. Đánh giá cuối khóa", h1))
s += bullets([
    "<b>Thực hành (70%):</b> vận hành buổi thờ phượng mô phỏng 30 phút với 2 Output, livestream và ít nhất 2 Action; giảng viên tạo 2 sự cố bất ngờ (đổi bài, mất NDI) để học viên xử lý.",
    "<b>Thiết kế (30%):</b> nộp sơ đồ hệ thống và checklist cho Hội Thánh của mình.",
    "Học viên đạt yêu cầu có thể làm <b>người hướng dẫn</b> khóa cơ bản tại Hội Thánh địa phương.",
])

s.append(P("10. Phát triển đội ngũ sau khóa học", h1))
s += bullets([
    "Mỗi Hội Thánh có ít nhất <b>1 người nắm hệ thống</b> (Output, mạng, livestream) và <b>1 người dự phòng</b>.",
    "Viết tài liệu nội bộ một trang: sơ đồ đấu nối, mật khẩu (lưu an toàn), các Action quan trọng, số điện thoại hỗ trợ.",
    "Họp ban kỹ thuật hằng tháng: rút kinh nghiệm, cập nhật Style, dọn dẹp thư viện bài hát.",
    "Kết nối với cộng đồng FreeShow (freeshow.app/docs, Discord, GitHub) để cập nhật tính năng mới và báo lỗi.",
])
s.append(Spacer(1, 8))
s.append(box(P("<b>Nguyên tắc:</b> công nghệ càng phức tạp thì càng cần đơn giản trong lúc vận hành. Mọi tự động hóa phải có "
               "<b>cách làm tay dự phòng</b>. Mục tiêu vẫn là giúp hội chúng thờ phượng Chúa, không phải trình diễn kỹ thuật.")))

doc = SimpleDocTemplate(sys.argv[1], pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=20 * mm,
                        title="Tài liệu huấn luyện FreeShow nâng cao", author="Ban Truyền Thông")
doc.build(s, onFirstPage=footer, onLaterPages=footer)
