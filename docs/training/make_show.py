"""Tạo file FreeShow (.show) để trình chiếu tài liệu huấn luyện cơ bản.

Dùng: python3 docs/training/make_show.py docs/training/FreeShow_Training_HoiThanh.show
Trong FreeShow: Ctrl/Cmd+I → "FreeShow Song/Presentation File" → chọn file .show.
"""
import base64
import json
import os
import random
import string
import sys
import time

NAVY = "#1F3A5F"
GOLD = "#C8963E"
WHITE = "#FFFFFF"
MUTED = "#C9D3E0"
FONT = "font-family:Arial;"

random.seed(20261108)
HINH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hinh")


def uid(n=11):
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=n))


def run(text, size, color=WHITE, bold=False, italic=False):
    st = f"{FONT}font-size:{size}px;color:{color};line-height:1.3em;"
    if bold:
        st += "font-weight:bold;"
    if italic:
        st += "font-style:italic;"
    return {"value": text, "style": st}


def line(runs, align="text-align: left;"):
    return {"align": align, "text": runs}


def box(style, lines, valign="align-items: flex-start;", fit="shrinkToFit"):
    item = {"type": "text", "style": style, "align": valign, "lines": lines}
    if fit:
        item["textFit"] = fit
    return item


def shape(style):
    return {"type": "text", "style": style, "align": "", "lines": [line([{"value": "", "style": ""}])]}


def rich(text, size, color=WHITE):
    """'**đậm** thường' → các run, phần trong ** ** in đậm màu vàng."""
    parts = text.split("**")
    return [run(p, size, GOLD if i % 2 else color, bold=bool(i % 2)) for i, p in enumerate(parts) if p]


def footer(label):
    return box("left:120px;top:1000px;width:1680px;height:50px;",
               [line([run(label, 26, MUTED)])], valign="", fit=None)


SLIDES = []  # (group, settings_color, items, notes)


def title_slide(title, subtitle, notes=""):
    items = [
        shape(f"left:0px;top:0px;width:30px;height:1080px;background-color:{GOLD};"),
        box("left:160px;top:330px;width:1600px;height:260px;", [line([run(title, 110, WHITE, bold=True)])], valign="align-items: flex-end;"),
        shape(f"left:160px;top:615px;width:260px;height:10px;background-color:{GOLD};"),
        box("left:160px;top:660px;width:1600px;height:200px;", [line([run(subtitle, 50, MUTED)])]),
    ]
    SLIDES.append((title, NAVY, items, notes))


def section(label, title, minutes, notes=""):
    items = [
        box("left:160px;top:300px;width:1600px;height:120px;", [line([run(label.upper(), 56, GOLD, bold=True)])], valign="align-items: flex-end;"),
        box("left:160px;top:430px;width:1600px;height:300px;", [line([run(title, 96, WHITE, bold=True)])]),
        box("left:160px;top:760px;width:1600px;height:80px;", [line([run(minutes, 40, MUTED)])], fit=None),
    ]
    SLIDES.append((label, NAVY, items, notes))


def content(title, bullets, foot, notes="", size=58):
    lines = [line([run("•  ", size, GOLD, bold=True)] + rich(b, size)) for b in bullets]
    items = [
        box("left:120px;top:70px;width:1680px;height:130px;", [line([run(title, 76, WHITE, bold=True)])], valign="align-items: flex-end;"),
        shape(f"left:120px;top:220px;width:180px;height:8px;background-color:{GOLD};"),
        box("left:120px;top:270px;width:1680px;height:710px;", lines),
        footer(foot),
    ]
    SLIDES.append((title, NAVY, items, notes))


def pairs(title, rows, foot, notes="", size=54):
    """Bảng 2 cột hiển thị dạng 'Khóa — mô tả'."""
    lines = [line([run(k, size, GOLD, bold=True), run("   " + v, size)]) for k, v in rows]
    items = [
        box("left:120px;top:70px;width:1680px;height:130px;", [line([run(title, 76, WHITE, bold=True)])], valign="align-items: flex-end;"),
        shape(f"left:120px;top:220px;width:180px;height:8px;background-color:{GOLD};"),
        box("left:120px;top:270px;width:1680px;height:710px;", lines),
        footer(foot),
    ]
    SLIDES.append((title, NAVY, items, notes))


def quote(text, foot, notes=""):
    items = [
        shape(f"left:160px;top:330px;width:12px;height:420px;background-color:{GOLD};"),
        box("left:220px;top:300px;width:1500px;height:480px;", [line(rich(text, 62))], valign="align-items: center;"),
        footer(foot),
    ]
    SLIDES.append((foot, NAVY, items, notes))


def img_size(path):
    """Đọc kích thước PNG/JPEG không cần thư viện ngoài."""
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return int.from_bytes(data[16:20], "big"), int.from_bytes(data[20:24], "big")
    i = 2
    while i < len(data):
        marker, ln = data[i + 1], int.from_bytes(data[i + 2:i + 4], "big")
        if marker in (0xC0, 0xC1, 0xC2):
            return int.from_bytes(data[i + 7:i + 9], "big"), int.from_bytes(data[i + 5:i + 7], "big")
        i += 2 + ln
    raise ValueError(path)


def media(name, left, top, max_w, max_h, border=False):
    """Item hình ảnh nhúng base64, đặt giữa khung (left, top, max_w, max_h) theo đúng tỉ lệ."""
    path = os.path.join(HINH, name)
    w, h = img_size(path)
    scale = min(max_w / w, max_h / h)
    bw, bh = round(w * scale), round(h * scale)
    x, y = left + (max_w - bw) // 2, top + (max_h - bh) // 2
    mime = "image/png" if name.endswith(".png") else "image/jpeg"
    with open(path, "rb") as f:
        src = f"data:{mime};base64," + base64.b64encode(f.read()).decode()
    style = f"left:{x}px;top:{y}px;width:{bw}px;height:{bh}px;"
    if border:
        style += f"border:4px solid {GOLD};border-radius:10px;overflow:hidden;"
    return {"type": "media", "style": style, "src": src, "fit": "contain"}


def picture(title, name, foot, notes="", border=True):
    """Slide có tiêu đề và một hình lớn (ảnh chụp màn hình hoặc sơ đồ)."""
    items = [
        box("left:120px;top:40px;width:1680px;height:120px;", [line([run(title, 68, WHITE, bold=True)])], valign="align-items: flex-end;"),
        shape(f"left:120px;top:175px;width:180px;height:8px;background-color:{GOLD};"),
        media(name, 120, 215, 1680, 770, border),
        footer(foot),
    ]
    SLIDES.append((title, NAVY, items, notes))


def diagram(title, name, foot, notes=""):
    picture(title, name, foot, notes, border=False)


# ---------------- Nội dung ----------------
T = "Huấn luyện FreeShow · Hội Thánh"

title_slide("Huấn luyện FreeShow", "Chương trình đào tạo ban truyền thông / trình chiếu cho các Hội Thánh",
            "Chào mừng học viên. Giới thiệu giảng viên, thời lượng 4 buổi, mời học viên mở laptop.")

content("FreeShow là gì?", [
    "Phần mềm trình chiếu **miễn phí, mã nguồn mở**: Windows, macOS, Linux",
    "Lời bài hát, Kinh Thánh, hình ảnh, video, đồng hồ đếm giờ",
    "Màn hình bục (Stage) cho ban hát, điều khiển từ điện thoại",
    "Không mất phí bản quyền, cài trên nhiều máy, dữ liệu nằm trên máy của mình",
], T)

content("Mục tiêu khóa huấn luyện", [
    "Mỗi Hội Thánh có ít nhất **2–3 người** tự tin vận hành trình chiếu",
    "Chuẩn bị trước một **Project**: bài hát, Kinh Thánh, thông báo, video",
    "Xử lý tình huống: đổi bài đột xuất, tắt màn hình, mất kết nối máy chiếu",
    "Dùng màn hình bục, điều khiển từ xa, đồng hồ, hợp âm cho ban nhạc",
], T)

content("Đối tượng tham gia", [
    "Ban trình chiếu / truyền thông, ban âm thanh – ánh sáng",
    "Trưởng ban hát, ban nhạc (màn hình bục và hợp âm)",
    "Mục sư, truyền đạo, thư ký Hội Thánh",
    "Yêu cầu: biết dùng máy tính cơ bản, nên mang laptop",
], T)

pairs("Chương trình 4 buổi", [
    ("Buổi 1", "Cài đặt, giao diện, Project – Show – Slide, Output (90′)"),
    ("Buổi 2", "Bài hát, import, Layout, hợp âm, Style / Theme (120′)"),
    ("Buổi 3", "Kinh Thánh, media, âm thanh, thông báo, Overlay (120′)"),
    ("Buổi 4", "Stage, Remote, đồng hồ, livestream, thực hành (120′)"),
], T, "Gợi ý: 2 ngày (mỗi ngày 2 buổi) hoặc 4 tối. Buổi cuối thực hành trên thiết bị của nhà thờ.")

# ---- Buổi 1
B1 = "Buổi 1 · Làm quen với FreeShow"
section("Buổi 1", "Làm quen với FreeShow", "90 phút")
content("Cài đặt", [
    "Tải tại **freeshow.app**, chọn đúng hệ điều hành (Mac: Apple chip hoặc Intel)",
    "Lần đầu mở: chọn ngôn ngữ và **thư mục lưu dữ liệu** dễ sao lưu",
    "Kết nối máy chiếu / TV: FreeShow tự nhận màn hình thứ hai",
    "Chọn màn hình xuất tại **Cài đặt → Outputs**",
], B1, "Cho học viên cài đặt ngay trên máy. Kiểm tra mọi người mở được phần mềm trước khi tiếp tục.")
picture("Cài đặt → Đầu ra (Outputs)", "anh-cai-dat-dau-ra.jpg", B1,
        "Bấm biểu tượng bánh răng (hoặc phím 5) → Đầu ra. Chọn màn hình xuất, bật Luôn ở trên cùng. Nút Đầu ra mới để thêm màn hình phụ.")
pairs("Các khái niệm cơ bản", [
    ("Project", "danh sách thứ tự cho một buổi nhóm"),
    ("Show", "một mục: bài hát, bài giảng, thông báo"),
    ("Slide", "một trang hiển thị trong Show"),
    ("Output", "cửa sổ ra máy chiếu / TV / livestream"),
    ("Style / Theme", "kiểu chữ, màu, nền dùng chung"),
], B1, "Ví dụ: Project “Thờ phượng Chúa nhật 09/11”, Show “Chúa Là Tình Yêu”, Slide “Phiên khúc 1”.")
diagram("Project → Show → Slide → Output", "so-do-khai-niem.png", B1,
        "Một Project chứa nhiều Show theo thứ tự chương trình; mỗi Show gồm nhiều Slide; slide được bấm sẽ hiện ra Output.")
content("Bố cục giao diện", [
    "**Trái:** danh sách Project và các Show",
    "**Giữa:** slide của Show đang chọn, bấm để đưa lên màn hình",
    "**Phải:** Preview và nút xóa nhanh từng lớp",
    "**Dưới (Drawer):** Show, Media, Âm thanh, Kinh Thánh, Overlay, Đồng hồ",
    "**Trên cùng:** chuyển Show / Edit / Stage / Cài đặt",
], B1, "Mở FreeShow lên và chỉ từng vùng trên màn hình thật.")
picture("Giao diện FreeShow", "anh-man-hinh-chinh.jpg", B1,
        "Trái: Project đang mở. Giữa: các slide của bài hát, slide đang chiếu có viền hồng. Phải: Preview, nút Xóa tất cả và các nút xóa từng lớp. Dưới: Drawer với các thẻ Bản trình chiếu, Phương tiện, Âm thanh, Lớp phủ, Kinh thánh.")
diagram("4 lớp hiển thị", "so-do-4-lop.png", B1,
        "Các lớp chồng lên nhau: nền ở dưới, slide ở giữa, lớp phủ trên cùng; âm thanh chạy riêng. Mỗi lớp xóa riêng bằng F1–F4, Esc xóa tất cả.")
quote("**Esc** (hoặc dấu chấm) xóa tất cả.\n**Ctrl/Cmd + L** khóa màn hình xuất để sửa mà hội chúng không thấy.", B1)

# ---- Buổi 2
B2 = "Buổi 2 · Bài hát thờ phượng"
section("Buổi 2", "Bài hát thờ phượng", "120 phút")
content("Tạo bài hát mới", [
    "Bấm **+ Tạo Show**, nhập tên, chọn danh mục",
    "Dán lời, để **một dòng trống** giữa các đoạn để tự chia slide",
    "Ghi **[Verse] [Chorus] [Bridge]** phía trên mỗi đoạn",
    "Mỗi slide **2–4 dòng**, chữ đủ lớn cho người ngồi cuối",
], B2, "Demo trực tiếp: dán lời một bài thánh ca quen thuộc.")
picture("Quick lyrics: dán lời bài hát", "anh-tao-bai-hat.jpg", B2,
        "Bản trình chiếu mới → nhập Tên, chọn Danh mục → Quick lyrics → dán lời, các đoạn cách nhau một dòng trống → Tạo.")
content("Nhập bài hát từ phần mềm khác", [
    "**Ctrl/Cmd + I** hoặc nút Import ở thẻ Shows để thấy đủ định dạng",
    "ProPresenter, EasyWorship, OpenLP, OpenSong, MediaShout…",
    "Văn bản .txt, ChordPro, CSV, PowerPoint, PDF, Canva",
    "Import trong Project chỉ có PDF, PowerPoint, văn bản, ChordPro",
], B2)
picture("Hộp thoại Nhập (Import)", "anh-nhap-import.jpg", B2,
        "Mở từ nút Nhập ở thẻ Bản trình chiếu. Kéo xuống để thấy thêm định dạng. File .show của FreeShow nhập ở ô Show trên cùng.")
content("Sắp xếp đoạn (Layout)", [
    "Một bài có nhiều Layout: “Chúa nhật” **V1–C–V2–C–B–C**, “Ngắn” **V1–C**",
    "Kéo thả để đổi thứ tự, lặp đoạn không cần gõ lại",
    "Thống nhất trước thứ tự với trưởng ban hát",
], B2)
content("Hợp âm và ghi chú", [
    "Thêm **hợp âm** ở chế độ Edit, chỉ hiện trên màn hình bục",
    "Đổi tông (transpose) nhanh khi người hát cần",
    "**Ghi chú** từng slide: “Hát chậm lại”, “Mời hội chúng đứng”",
], B2)
picture("Chế độ Chỉnh sửa", "anh-che-do-chinh-sua.jpg", B2,
        "Thẻ Slide để sửa chữ, font, cỡ chữ, viền, bóng. Thẻ Hợp âm để thêm hợp âm. Thẻ Chỉnh sửa văn bản để sửa nhanh toàn bộ lời.")
content("Giao diện thống nhất (Style)", [
    "Font có dấu tiếng Việt rõ ràng, chữ tương phản với nền, có viền / bóng",
    "Đặt **nền mặc định** để không phải gán cho từng bài",
    "Kiểm tra trên **máy chiếu thật**, màu laptop khác máy chiếu",
], B2)

# ---- Buổi 3
B3 = "Buổi 3 · Kinh Thánh, media và thông báo"
section("Buổi 3", "Kinh Thánh, media và thông báo", "120 phút")
content("Trình chiếu Kinh Thánh", [
    "Thẻ **Kinh Thánh**: nhập bản tiếng Việt (Truyền Thống 1925, Bản Dịch Mới)",
    "Gõ nhanh **Giăng 3:16** hoặc **Gi 3:16-18**, hoặc tìm theo từ khóa",
    "Chọn nhiều câu → tạo Show → thêm vào Project",
    "Hiển thị **hai bản dịch song song** cho Hội Thánh song ngữ",
], B3)
picture("Thẻ Kinh thánh", "anh-kinh-thanh.jpg", B3,
        "Trái: danh sách bản Kinh Thánh. Giữa: sách, chương, câu. Phải: xem trước và nút Convert to show để đưa vào Project.")
content("Hình ảnh, video, âm thanh", [
    "Thẻ **Media**: bấm một lần làm nền, kéo vào Project để phát theo thứ tự",
    "Video: lặp, tắt tiếng, tự chuyển slide khi kết thúc",
    "Thẻ **Âm thanh**: nhạc nền, playlist, âm lượng",
    "Dùng **camera** làm nền để chiếu người giảng lên màn hình lớn",
], B3)
content("Thông báo và Overlay", [
    "Show “Thông báo”, mỗi slide một tin, **tự chuyển sau 8–10 giây**",
    "**Overlay**: logo, tên & chức vụ người giảng, chữ chạy",
    "Overlay không mất khi đổi bài, xóa bằng **F3**",
], B3)
picture("Thẻ Lớp phủ", "anh-lop-phu.jpg", B3,
        "Có sẵn mẫu: đồng hồ, tên người giảng (lower third), hình mờ, vignette. Bấm Lớp phủ mới để tạo logo Hội Thánh.")

# ---- Buổi 4
B4 = "Buổi 4 · Tính năng hỗ trợ buổi nhóm"
section("Buổi 4", "Tính năng hỗ trợ buổi nhóm", "120 phút")
diagram("Kết nối qua trình duyệt", "so-do-ket-noi.png", B4, "Điện thoại/máy tính bảng phải cùng Wi-Fi. Địa chỉ 192.168.x.x:5510 và mật khẩu xem trong Cài đặt → Connection.")
content("Tính năng khác", [
    "**Đồng hồ:** đếm ngược trước giờ nhóm, giới hạn giờ giảng",
    "**Nhiều Output:** máy chiếu chính, TV sảnh, phòng thiếu nhi",
    "**Livestream:** NDI hoặc trình duyệt cho OBS → Facebook / YouTube",
    "**Lịch & Actions:** hẹn giờ, điều khiển bằng MIDI / bàn phím rời",
], B4)
content("Lưu ý kết nối", [
    "Thiết bị phải **cùng mạng Wi-Fi** với máy chạy FreeShow",
    "Địa chỉ dạng **192.168.x.x:5510**",
    "Địa chỉ và mật khẩu xem tại **Cài đặt → Connection**",
], B4)
picture("Cài đặt → Kết nối", "anh-cai-dat-ket-noi.jpg", B4,
        "Bật RemoteShow, StageShow, ControlShow, OutputShow tại đây. Bấm vào từng dòng để xem địa chỉ IP, cổng và mật khẩu.")
picture("Thiết kế màn hình Stage", "anh-san-khau-stage.jpg", B4,
        "Chế độ Sân khấu: bố cục cho ban hát gồm slide hiện tại (trên) và slide kế tiếp (dưới). Có thể thêm đồng hồ, ghi chú, hợp âm.")

# ---- Quy trình
Q = "Vận hành buổi thờ phượng"
section("Thực hành", "Vận hành một buổi thờ phượng", "Quy trình · phím tắt · sự cố")
diagram("Quy trình chuẩn", "so-do-quy-trinh.png", Q,
        "Trong buổi nhóm: theo dõi người hát để chuyển slide sớm nửa câu. Sau buổi nhóm: sao lưu tại Cài đặt → Sao lưu mỗi tuần.")
pairs("Phím tắt cần nhớ", [
    ("→ / Space / PageDown", "slide kế tiếp"),
    ("← / PageUp", "slide trước"),
    ("Esc hoặc .", "xóa tất cả"),
    ("F1 · F2 · F3 · F4", "xóa nền · chữ · lớp phủ · âm thanh"),
    ("Ctrl/Cmd + L", "khóa / mở khóa Output"),
    ("Ctrl/Cmd + Z", "hoàn tác"),
], Q, "FreeShow nhận phím mũi tên / PageUp / PageDown của bút trình chiếu không dây.")
pairs("Xử lý sự cố", [
    ("Màn hình không hiện", "kiểm tra HDMI, chọn lại Output, bật Output"),
    ("Lỗi dấu tiếng Việt", "đổi font (Arial, Roboto, Be Vietnam Pro), tệp UTF-8"),
    ("Remote không vào được", "cùng Wi-Fi, đúng IP và cổng, kiểm tra firewall"),
    ("Video giật / không tiếng", "dùng MP4 (H.264), kiểm tra thiết bị âm thanh"),
    ("Lỡ bấm sai slide", "bấm lại slide đúng, cần ẩn thì F2"),
], Q, size=50)

content("Bài tập thực hành", [
    "Tạo bài hát mới, đặt tên đoạn, tạo Layout",
    "Import bài hát / PowerPoint, kiểm tra dấu tiếng Việt",
    "Tạo Style chung, áp dụng cho 3 bài",
    "Show Kinh Thánh 5–8 câu (có thể song ngữ)",
    "Overlay tên người giảng + thông báo tự chạy",
    "Kết nối Stage và Remote",
    "Diễn tập trọn vẹn buổi thờ phượng 20 phút",
], Q, "Học viên làm theo nhóm 2 người, giảng viên đi kiểm tra từng nhóm.", size=52)
content("Phân công vai trò", [
    "**Trình chiếu chính:** chuẩn bị Project, vận hành buổi nhóm",
    "**Hỗ trợ / dự bị:** theo dõi Stage, chuẩn bị Kinh Thánh phát sinh",
    "**Phụ trách dữ liệu:** thư viện bài hát, Style, sao lưu",
    "**Luân phiên** để nhiều người cùng thành thạo",
], Q)
content("Tài nguyên tham khảo", [
    "**freeshow.app** · tải phần mềm",
    "**freeshow.app/docs** · hướng dẫn chính thức",
    "**freeshow.app/resources** · nền, Kinh Thánh, công cụ",
    "**github.com/ChurchApps/FreeShow** · mã nguồn, báo lỗi",
    "Nền miễn phí: Pexels, Pixabay, Unsplash, MotionBolt",
], Q, "Nhắc kiểm tra giấy phép hình/video, nhất là khi livestream.")
quote("Trình chiếu là một **mục vụ phục vụ**.\nChuẩn bị kỹ, giao diện đơn giản, chuyển slide đúng lúc.", "Lời kết")


# ---------------- Ghép show ----------------
def build():
    now = int(time.time() * 1000)
    slides, layout_slides = {}, []
    for group, color, items, notes in SLIDES:
        sid = uid()
        # tách "\n" trong run thành nhiều dòng
        for it in items:
            if "lines" not in it:
                continue
            new_lines = []
            for ln in it["lines"]:
                cur = []
                for r in ln["text"]:
                    chunks = r["value"].split("\n")
                    for i, c in enumerate(chunks):
                        if i:
                            new_lines.append({"align": ln["align"], "text": cur})
                            cur = []
                        cur.append({"value": c, "style": r["style"]})
                new_lines.append({"align": ln["align"], "text": cur})
            it["lines"] = new_lines
        slides[sid] = {"group": group, "color": GOLD, "settings": {"color": color}, "notes": notes, "items": items}
        layout_slides.append({"id": sid})
    layout_id = uid()
    show = {
        "name": "Huấn luyện FreeShow - Hội Thánh",
        "category": "presentation",
        "settings": {"activeLayout": layout_id, "template": None},
        "timestamps": {"created": now, "modified": now, "used": None},
        "meta": {"author": "Ban Truyền Thông"},
        "slides": slides,
        "layouts": {layout_id: {"name": "Mặc định", "notes": "", "slides": layout_slides}},
        "media": {},
    }
    return [uid(), show]


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "FreeShow_Training_HoiThanh.show"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(build(), f, ensure_ascii=False)
    print(f"{out}: {len(SLIDES)} slide")
