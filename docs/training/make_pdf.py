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
    c.drawString(20 * mm, 12 * mm, "Tài liệu huấn luyện FreeShow cho Hội Thánh")
    c.drawRightString(190 * mm, 12 * mm, f"Trang {d.page}")
    c.setStrokeColor(ACCENT)
    c.setLineWidth(0.8)
    c.line(20 * mm, 15 * mm, 190 * mm, 15 * mm)
    c.restoreState()


s = []

# ---------- Trang 1 ----------
s += [
    P("Tài liệu huấn luyện FreeShow", title),
    P("Chương trình đào tạo ban truyền thông / trình chiếu cho các Hội Thánh", subtitle),
]
s.append(box(P(
    "<b>FreeShow</b> là phần mềm trình chiếu <b>miễn phí, mã nguồn mở</b>, chạy trên Windows, macOS và Linux. "
    "Phần mềm được thiết kế cho các buổi thờ phượng: trình chiếu lời bài hát, câu Kinh Thánh, hình ảnh, video, "
    "đồng hồ đếm giờ, màn hình cho người hướng dẫn trên bục (stage display), và cho phép điều khiển từ điện thoại. "
    "Hội Thánh không mất phí bản quyền, có thể cài trên nhiều máy, và dữ liệu nằm trên máy của mình.")))
s.append(Spacer(1, 8))

s.append(P("1. Mục tiêu khóa huấn luyện", h1))
s += bullets([
    "Mỗi Hội Thánh có ít nhất <b>2–3 người</b> tự tin vận hành trình chiếu cho một buổi nhóm thờ phượng.",
    "Biết chuẩn bị trước một <b>chương trình (Project)</b> gồm bài hát, câu Kinh Thánh, thông báo và video.",
    "Biết xử lý các tình huống thường gặp trong lúc nhóm (đổi bài đột xuất, tắt màn hình, mất kết nối máy chiếu).",
    "Biết dùng các tính năng hỗ trợ: màn hình bục giảng, điều khiển từ xa, đồng hồ, hợp âm cho ban nhạc.",
])

s.append(P("2. Đối tượng tham gia", h1))
s += bullets([
    "Thành viên ban trình chiếu / truyền thông, ban âm thanh – ánh sáng.",
    "Trưởng ban hát, ban nhạc (để hiểu màn hình bục và hợp âm).",
    "Mục sư, truyền đạo, thư ký Hội Thánh muốn tự chuẩn bị bài giảng và thông báo.",
    "Yêu cầu: biết sử dụng máy tính cơ bản. Mỗi học viên nên mang theo laptop (nếu có).",
])

s.append(P("3. Chương trình tổng quát", h1))
s.append(table([
    ["Buổi", "Nội dung", "Thời lượng"],
    ["1", "Cài đặt, làm quen giao diện, khái niệm Project – Show – Slide, màn hình xuất (Output)", "90 phút"],
    ["2", "Bài hát: tạo mới, nhập (import) từ phần mềm khác, sắp xếp đoạn, hợp âm, giao diện (Style / Theme)", "120 phút"],
    ["3", "Kinh Thánh, hình ảnh, video, âm thanh, thông báo và lớp phủ (Overlay)", "120 phút"],
    ["4", "Màn hình bục (Stage), điều khiển từ xa, đồng hồ, livestream; thực hành một buổi nhóm hoàn chỉnh", "120 phút"],
], [18 * mm, 125 * mm, 27 * mm]))
s.append(Spacer(1, 6))
s.append(P("Gợi ý: tổ chức 2 ngày (mỗi ngày 2 buổi) hoặc 4 tối trong tuần. Buổi cuối nên thực hành trên chính thiết bị của nhà thờ.", note))

s.append(PageBreak())

# ---------- Trang 2 ----------
s.append(P("4. Buổi 1 — Làm quen với FreeShow", h1))
s.append(P("4.1 Cài đặt", h2))
s += bullets([
    "Tải bản cài đặt tại <b>freeshow.app</b> (chọn đúng hệ điều hành). Trên macOS có bản cho chip Apple (M1/M2/M3…) và Intel.",
    "Lần đầu mở, chọn ngôn ngữ, thư mục lưu dữ liệu (nên chọn thư mục dễ sao lưu, ví dụ trong Documents hoặc thư mục đồng bộ đám mây).",
    "Kết nối máy chiếu / TV: FreeShow tự nhận màn hình thứ hai. Vào <b>Cài đặt → Outputs</b> để chọn màn hình xuất.",
])
s.append(P("4.2 Các khái niệm cơ bản", h2))
s.append(table([
    ["Khái niệm", "Ý nghĩa", "Ví dụ"],
    ["Project (Dự án)", "Danh sách thứ tự cho một buổi nhóm", "“Thờ phượng Chúa nhật 09/11”"],
    ["Show", "Một mục trình chiếu: bài hát, bài giảng, thông báo…", "Bài hát “Chúa Là Tình Yêu”"],
    ["Slide", "Một trang hiển thị trong Show", "Phiên khúc 1, Điệp khúc"],
    ["Output", "Cửa sổ hiển thị ra máy chiếu / TV / livestream", "Màn hình chính, màn hình phụ"],
    ["Style / Theme", "Kiểu chữ, màu, nền, vị trí chữ áp dụng chung", "Chữ trắng viền đen, nền tối"],
], [32 * mm, 78 * mm, 60 * mm]))
s.append(P("4.3 Bố cục giao diện", h2))
s += bullets([
    "<b>Bên trái:</b> danh sách Project và các Show trong Project đang mở.",
    "<b>Ở giữa:</b> các slide của Show đang chọn — bấm vào slide để đưa lên màn hình.",
    "<b>Bên phải:</b> khung xem trước (Preview) những gì đang hiển thị, cùng các nút xóa nhanh từng lớp.",
    "<b>Phía dưới (Drawer):</b> thư viện Show, Media, Âm thanh, Kinh Thánh, Lớp phủ, Đồng hồ, Lịch…",
    "<b>Thanh trên cùng:</b> chuyển giữa chế độ Trình chiếu (Show), Chỉnh sửa (Edit), Màn hình bục (Stage), Cài đặt.",
])
s.append(P("4.4 Nguyên tắc “4 lớp hiển thị”", h2))
s.append(P("Màn hình xuất gồm các lớp chồng lên nhau, mỗi lớp có thể xóa riêng bằng phím tắt:"))
s.append(table([
    ["Lớp", "Nội dung", "Phím xóa"],
    ["Nền (Background)", "Hình ảnh, video nền, camera", "F1"],
    ["Slide", "Lời bài hát, câu Kinh Thánh, chữ", "F2"],
    ["Lớp phủ (Overlay)", "Logo, tên người giảng, thông báo chạy chữ", "F3"],
    ["Âm thanh", "Nhạc nền, bài hát, micro", "F4"],
], [45 * mm, 95 * mm, 30 * mm]))
s.append(Spacer(1, 5))
s.append(box(P("<b>Mẹo quan trọng:</b> phím <b>Esc</b> (hoặc dấu chấm <b>.</b>) xóa tất cả — dùng khi cần tắt màn hình ngay lập tức. "
               "Phím <b>Ctrl/Cmd + L</b> khóa màn hình xuất, giúp chỉnh sửa trong lúc nhóm mà không làm thay đổi những gì hội chúng đang thấy.")))

s.append(PageBreak())

# ---------- Trang 3 ----------
s.append(P("5. Buổi 2 — Bài hát thờ phượng", h1))
s.append(P("5.1 Tạo bài hát mới", h2))
s += bullets([
    "Bấm <b>+ Tạo Show</b>, nhập tên bài, chọn danh mục (ví dụ: Thánh ca, Tôn vinh, Thiếu nhi).",
    "Dán toàn bộ lời bài hát vào ô văn bản. Để <b>một dòng trống</b> giữa các đoạn — FreeShow sẽ tự chia thành slide.",
    "Đặt tên đoạn bằng cách ghi <b>[Verse]</b>, <b>[Chorus]</b>, <b>[Bridge]</b> phía trên mỗi đoạn để dễ sắp xếp.",
    "Nên giữ mỗi slide <b>2–4 dòng</b>, chữ đủ lớn để người ngồi cuối nhà thờ đọc được.",
])
s.append(P("5.2 Nhập bài hát từ phần mềm khác", h2))
s.append(P("Hội Thánh đang dùng phần mềm khác có thể chuyển dữ liệu sang FreeShow qua menu <b>Tập tin → Import</b>. Các định dạng được hỗ trợ gồm:"))
s.append(table([
    ["Nhóm", "Định dạng / phần mềm"],
    ["Phần mềm trình chiếu", "ProPresenter, EasyWorship, OpenLP, OpenSong, MediaShout, SongBeamer, Quelea, VideoPsalm, SoftProjector, VerseVIEW, EasySlides"],
    ["Văn bản & hợp âm", "Tệp văn bản (.txt), ChordPro, CSV"],
    ["Trình chiếu văn phòng", "PowerPoint (.pptx), PDF, Canva, chuỗi hình ảnh"],
    ["Kinh Thánh", "Zefania XML, OSIS, Beblia, OpenSong"],
], [45 * mm, 125 * mm]))
s.append(P("<b>Lưu ý:</b> nút <b>Import</b> nằm trong một Project chỉ hiện PDF, PowerPoint, tệp văn bản và ChordPro, để thêm nhanh vào Project đang mở. Muốn thấy đầy đủ định dạng (ProPresenter, EasyWorship, OpenLP...), nhấn <b>Ctrl+I</b> hoặc bấm nút Import ở thẻ <b>Shows</b>.", note))
s.append(P("5.3 Sắp xếp thứ tự đoạn (Layout)", h2))
s += bullets([
    "Một bài hát có thể có nhiều <b>Layout</b>: ví dụ “Chúa nhật” (V1 – C – V2 – C – B – C) và “Ngắn” (V1 – C).",
    "Kéo thả slide để đổi thứ tự; một đoạn có thể lặp lại nhiều lần mà không cần gõ lại.",
    "Trưởng ban hát nên thống nhất trước với người trình chiếu về thứ tự đoạn hát.",
])
s.append(P("5.4 Hợp âm và ghi chú", h2))
s += bullets([
    "Ở chế độ Chỉnh sửa có thể thêm <b>hợp âm</b> trên lời bài hát. Hợp âm chỉ hiện trên màn hình bục cho ban nhạc, không hiện cho hội chúng.",
    "Có thể đổi tông (transpose) nhanh khi người hát chính cần.",
    "Thêm <b>ghi chú</b> cho từng slide (ví dụ: “Hát chậm lại”, “Mời hội chúng đứng”) để hiện trên màn hình bục.",
])
s.append(P("5.5 Giao diện thống nhất (Style / Theme)", h2))
s += bullets([
    "Tạo một <b>Style</b> chung cho Hội Thánh: font chữ có dấu tiếng Việt rõ ràng, màu chữ tương phản với nền, có viền/bóng chữ.",
    "Đặt <b>nền mặc định</b> (ảnh hoặc video chuyển động nhẹ) để không phải gán nền cho từng bài.",
    "Kiểm tra trên máy chiếu thật: màu trên màn hình laptop thường khác với máy chiếu.",
])

s.append(PageBreak())

# ---------- Trang 4 ----------
s.append(P("6. Buổi 3 — Kinh Thánh, media và thông báo", h1))
s.append(P("6.1 Trình chiếu Kinh Thánh", h2))
s += bullets([
    "Mở thẻ <b>Kinh Thánh</b> ở phần dưới. Nhập bản Kinh Thánh tiếng Việt (ví dụ Bản Truyền Thống 1925, Bản Dịch Mới) từ tệp hoặc tải trực tuyến.",
    "Gõ nhanh tham chiếu như <b>Giăng 3:16</b> hoặc <b>Gi 3:16-18</b> để tìm câu; có thể tìm theo từ khóa.",
    "Chọn nhiều câu rồi bấm để tạo thành Show, thêm vào Project của bài giảng.",
    "Có thể hiển thị <b>hai bản dịch song song</b> (ví dụ tiếng Việt và tiếng Anh) cho Hội Thánh song ngữ.",
])
s.append(P("6.2 Hình ảnh, video và âm thanh", h2))
s += bullets([
    "Thẻ <b>Media</b>: thêm thư mục hình/video của Hội Thánh. Bấm một lần để làm nền, kéo vào Project để phát theo thứ tự.",
    "Video có thể đặt lặp lại, tắt tiếng, hoặc tự chuyển slide khi video kết thúc.",
    "Thẻ <b>Âm thanh</b>: phát nhạc nền trước giờ nhóm, tạo danh sách phát (playlist), điều chỉnh âm lượng.",
    "Có thể hiển thị <b>camera</b> hoặc webcam làm nền (ví dụ quay trực tiếp người giảng lên màn hình lớn).",
])
s.append(P("6.3 Thông báo và lớp phủ (Overlay)", h2))
s += bullets([
    "Tạo Show “Thông báo” với mỗi slide một tin; đặt <b>tự chuyển slide</b> sau 8–10 giây để chạy vòng trước giờ nhóm.",
    "Tạo <b>Overlay</b> cho logo Hội Thánh, tên & chức vụ người giảng (lower third), dòng chữ chạy.",
    "Overlay hiển thị trên cùng, không bị mất khi chuyển bài hát — xóa bằng <b>F3</b>.",
])

s.append(P("7. Buổi 4 — Tính năng hỗ trợ buổi nhóm", h1))
s.append(table([
    ["Tính năng", "Công dụng trong Hội Thánh", "Cách truy cập"],
    ["Màn hình bục (Stage)", "Cho người hướng dẫn, ban hát thấy slide hiện tại, slide kế tiếp, hợp âm, ghi chú, đồng hồ", "Trình duyệt trên TV/máy tính bảng: cổng 5511"],
    ["Điều khiển từ xa (Remote)", "Người giảng hoặc trưởng ban tự chuyển slide bằng điện thoại", "Trình duyệt trên điện thoại: cổng 5510"],
    ["Controller", "Bảng điều khiển đơn giản trên máy tính bảng", "Cổng 5512"],
    ["Đồng hồ (Timers)", "Đếm ngược trước giờ nhóm, giới hạn thời gian bài giảng", "Thẻ Đồng hồ ở phần dưới"],
    ["Nhiều màn hình xuất", "Máy chiếu chính, TV sảnh, màn hình phòng thiếu nhi với nội dung khác nhau", "Cài đặt → Outputs"],
    ["Livestream", "Xuất hình qua NDI / trình duyệt (cổng 5513) cho OBS để phát Facebook/YouTube", "Cài đặt → Outputs → NDI"],
    ["Lịch & thao tác tự động", "Hẹn giờ bật Project, điều khiển bằng MIDI/bàn phím rời", "Thẻ Lịch, Actions"],
], [36 * mm, 82 * mm, 52 * mm]))
s.append(Spacer(1, 4))
s.append(P("Lưu ý: điện thoại / máy tính bảng phải kết nối <b>cùng mạng Wi-Fi</b> với máy chạy FreeShow. Địa chỉ truy cập (dạng 192.168.x.x:5510) và mật khẩu xem trong <b>Cài đặt → Connection</b>.", note))

s.append(PageBreak())

# ---------- Trang 5 ----------
s.append(P("8. Quy trình chuẩn cho một buổi thờ phượng", h1))
s.append(table([
    ["Thời điểm", "Việc cần làm"],
    ["Trước 2–3 ngày", "Nhận danh sách bài hát, câu Kinh Thánh, thông báo. Tạo Project mới, thêm đầy đủ các Show theo thứ tự chương trình. Kiểm tra chính tả lời bài hát."],
    ["Trước 30 phút", "Bật máy, kết nối máy chiếu, kiểm tra Output. Mở Project. Bật Stage cho ban hát, kết nối Remote nếu người giảng dùng. Chạy nhạc nền và slide thông báo, bật đồng hồ đếm ngược."],
    ["Trong buổi nhóm", "Theo dõi người hát để chuyển slide <b>đúng lúc (sớm nửa câu)</b>. Dùng F1–F4 để xóa từng lớp, Esc khi cần tắt hết. Khóa Output (Ctrl/Cmd + L) khi cần sửa nhanh."],
    ["Sau buổi nhóm", "Ghi chú các lỗi gặp phải, cập nhật lời bài hát nếu sai. Sao lưu dữ liệu (Cài đặt → Sao lưu) mỗi tuần."],
], [32 * mm, 138 * mm]))

s.append(P("9. Phím tắt cần nhớ", h1))
s.append(table([
    ["Phím", "Chức năng", "Phím", "Chức năng"],
    ["→ / Space / PageDown", "Slide kế tiếp", "F1", "Xóa nền"],
    ["← / PageUp", "Slide trước", "F2", "Xóa slide (chữ)"],
    ["Esc hoặc .", "Xóa tất cả", "F3", "Xóa lớp phủ"],
    ["Ctrl/Cmd + L", "Khóa / mở khóa Output", "F4", "Xóa âm thanh"],
    ["Ctrl/Cmd + Z", "Hoàn tác (undo)", "F5", "Chuyển tiếp Output"],
], [38 * mm, 47 * mm, 25 * mm, 60 * mm]))
s.append(Spacer(1, 4))
s.append(P("Có thể dùng <b>bút trình chiếu (presenter clicker)</b> không dây — FreeShow nhận các phím mũi tên / PageUp / PageDown của bút."))

s.append(P("10. Xử lý sự cố thường gặp", h1))
s.append(table([
    ["Hiện tượng", "Cách xử lý"],
    ["Màn hình chiếu không hiện gì", "Kiểm tra cáp HDMI; vào Cài đặt → Outputs chọn lại đúng màn hình; bấm nút bật Output trên thanh trên cùng."],
    ["Chữ tiếng Việt bị lỗi dấu", "Đổi sang font hỗ trợ tiếng Việt (Arial, Roboto, Be Vietnam Pro, Noto Sans); kiểm tra tệp import dùng mã UTF-8."],
    ["Điện thoại không vào được Remote", "Kiểm tra cùng mạng Wi-Fi, đúng địa chỉ IP và cổng; tường lửa (firewall) có thể đang chặn FreeShow."],
    ["Video giật, không có tiếng", "Dùng định dạng MP4 (H.264); kiểm tra thiết bị âm thanh xuất ra trong Cài đặt."],
    ["Khung Import thiếu ProPresenter, EasyWorship...", "Do đang mở Import từ trong Project (chỉ có PDF, PowerPoint, văn bản, ChordPro). Nhấn Ctrl+I hoặc dùng nút Import ở thẻ Shows để thấy đủ định dạng."],
    ["Lỡ bấm sai slide", "Bấm lại slide đúng ngay, không cần xóa. Nếu cần tạm ẩn, nhấn F2."],
], [48 * mm, 122 * mm]))

s.append(PageBreak())

# ---------- Trang 6 ----------
s.append(P("11. Bài tập thực hành", h1))
s.append(P("Mỗi học viên (hoặc nhóm 2 người) hoàn thành các bài sau, giảng viên kiểm tra và góp ý:"))
s.append(table([
    ["#", "Bài tập", "Tiêu chí đạt"],
    ["1", "Tạo bài hát mới từ lời có sẵn, đặt tên đoạn và tạo Layout theo thứ tự trưởng ban hát đưa ra", "Đúng thứ tự, mỗi slide 2–4 dòng"],
    ["2", "Import một tệp bài hát/PowerPoint từ phần mềm cũ của Hội Thánh", "Chữ hiển thị đúng dấu tiếng Việt"],
    ["3", "Tạo Style chung cho Hội Thánh và áp dụng cho 3 bài hát", "Đồng nhất, dễ đọc từ cuối phòng"],
    ["4", "Tạo Show Kinh Thánh cho bài giảng (5–8 câu, có thể song ngữ)", "Tìm nhanh, hiển thị đúng tham chiếu"],
    ["5", "Tạo Overlay tên người giảng và slide thông báo tự chạy", "Overlay bật/tắt độc lập bằng F3"],
    ["6", "Kết nối Stage trên máy tính bảng và Remote trên điện thoại", "Thấy slide kế tiếp và đồng hồ"],
    ["7", "Diễn tập trọn vẹn một buổi thờ phượng 20 phút theo Project đã chuẩn bị", "Không có khoảng trống, chuyển slide đúng lúc"],
], [10 * mm, 102 * mm, 58 * mm]))

s.append(P("12. Phân công vai trò đề xuất", h1))
s += bullets([
    "<b>Người trình chiếu chính:</b> chuẩn bị Project, vận hành trong buổi nhóm.",
    "<b>Người hỗ trợ / dự bị:</b> theo dõi Stage, chuẩn bị Kinh Thánh khi người giảng đọc thêm câu ngoài dự kiến, thay thế khi người chính vắng.",
    "<b>Người phụ trách dữ liệu:</b> quản lý thư viện bài hát, Style chung, sao lưu hàng tuần.",
    "Nên luân phiên để nhiều người cùng thành thạo, tránh phụ thuộc vào một người.",
])

s.append(P("13. Tài nguyên tham khảo", h1))
s += bullets([
    "Trang chủ & tải phần mềm: <b>freeshow.app</b>",
    "Hướng dẫn sử dụng chính thức: <b>freeshow.app/docs</b>",
    "Mã nguồn & báo lỗi: <b>github.com/ChurchApps/FreeShow</b>",
    "Cộng đồng hỗ trợ: Discord của FreeShow (liên kết trên trang chủ).",
])
s.append(Spacer(1, 8))
s.append(box(P("<b>Lời kết:</b> Trình chiếu là một mục vụ phục vụ — mục tiêu là giúp hội chúng tập trung thờ phượng Chúa, "
               "không phải gây chú ý vào màn hình. Chuẩn bị kỹ, giao diện đơn giản, chuyển slide đúng lúc là ba yếu tố quan trọng nhất.")))

doc = SimpleDocTemplate(sys.argv[1], pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=20 * mm,
                        title="Tài liệu huấn luyện FreeShow cho Hội Thánh", author="Ban Truyền Thông")
doc.build(s, onFirstPage=footer, onLaterPages=footer)
