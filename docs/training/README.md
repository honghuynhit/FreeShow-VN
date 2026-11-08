# Tài liệu huấn luyện FreeShow cho Hội Thánh

- [FreeShow_Training_HoiThanh.pdf](FreeShow_Training_HoiThanh.pdf): tài liệu 7 trang (A4) cho chương trình đào tạo 4 buổi.
- [make_pdf.py](make_pdf.py): script tạo lại file PDF bằng reportlab.
- [FreeShow_Training_NangCao.pdf](FreeShow_Training_NangCao.pdf): tài liệu nâng cao 6 trang, 4 buổi A–D, dành cho người đã qua khóa cơ bản.
- [make_pdf_nang_cao.py](make_pdf_nang_cao.py): script tạo lại PDF nâng cao.
- [FreeShow_Training_HoiThanh.show](FreeShow_Training_HoiThanh.show): bài trình chiếu khóa cơ bản (43 slide, có ảnh chụp giao diện và sơ đồ nhúng sẵn) để mở thẳng trong FreeShow. Import: thẻ Bản trình chiếu → Nhập → Show.
- [make_show.py](make_show.py): script tạo lại file .show (chỉ cần Python 3).
- [hinh/](hinh/): ảnh chụp giao diện (`anh-*.jpg`) và sơ đồ (`so-do-*.svg`, kèm bản `.png` đã dựng) dùng trong file .show.

## Nội dung khóa nâng cao

1. Buổi A: nhiều Output, Stage layouts, NDI / OMT / Blackmagic / WebRTC / RTMP, mô hình livestream với OBS
2. Buổi B: Actions, Triggers, Conditions, MIDI, Companion / Stream Deck, API (WebSocket 5505, REST 5506, OSC), Variables, Dynamic values, Timeline, Timecode, Lịch
3. Buổi C: Profiles, Cloud sync, sao lưu, Planning Center / ChurchApps / Canva, phụ đề trực tiếp, AI nhận dạng giọng nói
4. Buổi D: 3 mô hình hệ thống, checklist kỹ thuật, sự cố nâng cao, bài tập, đánh giá cuối khóa

## Nội dung khóa cơ bản

1. Mục tiêu, đối tượng, chương trình 4 buổi
2. Buổi 1: cài đặt, giao diện, Project / Show / Slide / Output, 4 lớp hiển thị
3. Buổi 2: bài hát, import, Layout, hợp âm, Style / Theme
4. Buổi 3: Kinh Thánh, media, âm thanh, thông báo, Overlay
5. Buổi 4: Stage, Remote, Controller, đồng hồ, nhiều màn hình, livestream
6. Quy trình buổi thờ phượng, phím tắt, xử lý sự cố
7. Bài tập thực hành, phân công vai trò, tài nguyên (kèm cách tìm tài nguyên tại freeshow.app/resources)

## Tạo lại PDF

Cần Python 3 và `reportlab`. Script dùng font Arial có sẵn trên macOS (`/System/Library/Fonts/Supplemental/`).
Trên Windows hoặc Linux, sửa biến `F` trong script để trỏ tới thư mục font của máy.

```bash
pip install reportlab
python3 docs/training/make_pdf.py docs/training/FreeShow_Training_HoiThanh.pdf
python3 docs/training/make_pdf_nang_cao.py docs/training/FreeShow_Training_NangCao.pdf
```
