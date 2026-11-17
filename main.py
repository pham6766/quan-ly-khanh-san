import json
import os

# Khởi tạo các biến toàn cục quản lý dữ liệu
danh_sach_phong = []
doanh_thu_tong = 0.0
TEN_FILE = "data.txt"

def luu_du_lieu():
    # Ghi lại danh sách phòng ra file (mode: w+)
    try:
        data_to_save = {
            "danh_sach_phong": danh_sach_phong,
            "doanh_thu_tong": doanh_thu_tong
        }
        with open(TEN_FILE, "w+", encoding="utf-8") as file:
            json.dump(data_to_save, file, ensure_ascii=False, indent=4)
        print("Đã đồng bộ dữ liệu vào file data.txt (mode: w+) thành công!")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi lưu file: {e}")

def doc_du_lieu():
    # Lấy dữ liệu phòng từ file và lưu vào list
    global danh_sach_phong, doanh_thu_tong
    if not os.path.exists(TEN_FILE):
        return
    try:
        with open(TEN_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            danh_sach_phong = data.get("danh_sach_phong", [])
            doanh_thu_tong = data.get("doanh_thu_tong", 0.0)
    except Exception as e:
        print(f"Lỗi đọc file: {e}")

def them_phong():
    print("\n--- THÊM PHÒNG MỚI ---")
    # Lấy dữ liệu từ file và lưu vào list trước khi kiểm tra trùng
    doc_du_lieu()
    
    ma_phong = input("Nhập mã phòng: ").strip()
    if not ma_phong:
        print("Lỗi: Mã phòng không được để trống!")
        return
        
    # Kiểm tra mã phòng trùng
    for p in danh_sach_phong:
        if p["ma_phong"] == ma_phong:
            print("Lỗi: Mã phòng đã tồn tại!")
            return
            
    try:
        so_phong = input("Nhập số phòng: ").strip()
        loai_phong = input("Nhập loại phòng: ").strip()
        gia_phong = float(input("Nhập giá phòng (VNĐ): "))
        if gia_phong <= 0:
            print("Lỗi: Giá phòng phải lớn hơn 0!")
            return
            
        suc_chua = int(input("Nhập sức chứa (người): "))
        if suc_chua <= 0:
            print("Lỗi: Sức chứa phải lớn hơn 0!")
            return

        phong_moi = {
            "ma_phong": ma_phong,
            "so_phong": so_phong,
            "loai_phong": loai_phong,
            "gia_phong": gia_phong,
            "suc_chua": suc_chua,
            "trang_thai": "Trống",
            "khach_hang": {}
        }
        danh_sach_phong.append(phong_moi)
        # Ghi lại danh sách phòng ra file (mode: w+)
        luu_du_lieu()
        print("Thêm phòng thành công!")
    except ValueError:
        print("Lỗi: Giá phòng và sức chứa phải là số hợp lệ!")

def hien_thi_phong():
    print("\n--- DANH SÁCH PHÒNG ---")
    if not danh_sach_phong:
        print("Hệ thống hiện chưa có phòng nào.")
        return
        
    print(f"{'Mã':<8} | {'Số phòng':<10} | {'Loại':<10} | {'Giá (VNĐ)':<15} | {'Sức chứa':<10} | {'Trạng thái'}")
    print("-" * 80)
    for p in danh_sach_phong:
        print(f"{p['ma_phong']:<8} | {p['so_phong']:<10} | {p['loai_phong']:<10} | {p['gia_phong']:<15.0f} | {p['suc_chua']:<10} | {p['trang_thai']}")

def cap_nhat_phong():
    # 1. Lấy danh sách phòng từ file & 2. Lưu vào list
    doc_du_lieu()
    
    ma_phong = input("Nhập mã phòng cần cập nhật: ").strip()
    # 3. Check điều kiện để cập nhật phòng trong danh sách
    for p in danh_sach_phong:
        if p["ma_phong"] == ma_phong:
            print(f"Đang cập nhật cho phòng: {ma_phong}")
            try:
                p["so_phong"] = input(f"Nhập số phòng mới (hiện tại: {p['so_phong']}): ").strip() or p["so_phong"]
                p["loai_phong"] = input(f"Nhập loại phòng mới (hiện tại: {p['loai_phong']}): ").strip() or p["loai_phong"]

                gia_moi = input(f"Nhập giá phòng mới (hiện tại: {p['gia_phong']}): ").strip()
                if gia_moi:
                    gia_val = float(gia_moi)
                    if gia_val <= 0:
                        print("Lỗi: Giá phòng phải lớn hơn 0!")
                        return
                    p["gia_phong"] = gia_val

                suc_chua_moi = input(f"Nhập sức chứa mới (hiện tại: {p['suc_chua']}): ").strip()
                if suc_chua_moi:
                    sc_val = int(suc_chua_moi)
                    if sc_val <= 0:
                        print("Lỗi: Sức chứa phải lớn hơn 0!")
                        return
                    p["suc_chua"] = sc_val

                # 4. Ghi lại danh sách phòng ra file (mode: w+)
                luu_du_lieu()
                print("Cập nhật thông tin phòng thành công!")
            except ValueError:
                print("Lỗi: Giá và sức chứa phải là số!")
            return
    print("Lỗi: Không tìm thấy mã phòng!")

def xoa_phong():
    # 1. Lấy danh sách phòng từ file & 2. Lưu vào list
    doc_du_lieu()
    
    ma_phong = input("Nhập mã phòng cần xóa: ").strip()
    # 3. Check điều kiện để xóa phòng khỏi danh sách
    for p in danh_sach_phong:
        if p["ma_phong"] == ma_phong:
            if p["trang_thai"] != "Trống":
                print("Lỗi: Phòng đang có khách, không thể xóa!")
                return
            danh_sach_phong.remove(p)
            
            # 4. Ghi lại danh sách phòng ra file (mode: w+)
            luu_du_lieu()
            print("Xóa phòng thành công!")
            return
    print("Lỗi: Không tìm thấy mã phòng!")

def tim_kiem():
    tu_khoa = input("Nhập từ khóa tìm kiếm (Mã phòng/Mã KH): ").strip().lower()
    ket_qua = []
    
    for p in danh_sach_phong:
        ma_kh = p["khach_hang"].get("ma_kh", "").lower() if p["khach_hang"] else ""
        if tu_khoa in p["ma_phong"].lower() or tu_khoa in ma_kh:
            ket_qua.append(p)
            
    if ket_qua:
        print("\n--- KẾT QUẢ TÌM KIẾM ---")
        for p in ket_qua:
            ma_kh_hien_thi = p["khach_hang"].get("ma_kh", "Không có") if p["khach_hang"] else "Không có"
            print(f"Mã phòng: {p['ma_phong']} | Mã KH: {ma_kh_hien_thi} | Số: {p['so_phong']} | Trạng thái: {p['trang_thai']}")
    else:
        print("Không tìm thấy kết quả nào phù hợp!")

def sap_xep():
    doc_du_lieu()
    
    if not danh_sach_phong:
        print("Hệ thống hiện chưa có phòng nào để sắp xếp.")
        return

    print("\n--- SẮP XẾP DANH SÁCH PHÒNG ---")
    print("1. Sắp xếp theo Giá phòng (Tăng dần)")
    print("2. Sắp xếp theo Sức chứa (Tăng dần)")
    print("3. Sắp xếp theo Số phòng (A-Z)")
    chon = input("Chọn tiêu chí sắp xếp (1-3): ").strip()
    

    if chon == '1':
        danh_sach_phong.sort(key=lambda x: x["gia_phong"])
        print("\n=> Đã sắp xếp danh sách theo Giá phòng tăng dần.")
    elif chon == '2':
        danh_sach_phong.sort(key=lambda x: x["suc_chua"])
        print("\n=> Đã sắp xếp danh sách theo Sức chứa tăng dần.")
    elif chon == '3':
        danh_sach_phong.sort(key=lambda x: str(x["so_phong"]))
        print("\n=> Đã sắp xếp danh sách theo Số phòng.")
    else:
        print("Lỗi: Lựa chọn không hợp lệ!")
        return  
    hien_thi_phong()
    luu_du_lieu()

def dat_phong():
    doc_du_lieu()
    ma_phong = input("Nhập mã phòng muốn đặt: ").strip()
    for p in danh_sach_phong:
        if p["ma_phong"] == ma_phong:
            if p["trang_thai"] != "Trống":
                print("Lỗi: Đặt phòng thất bại, phòng đã có khách!")
                return
            
            ma_kh = input("Nhập mã khách hàng: ").strip()
            ho_ten = input("Nhập họ tên khách hàng: ").strip()
            sdt = input("Nhập số điện thoại: ").strip()
            cccd = input("Nhập CCCD: ").strip()
            
            if not sdt or not cccd:
                print("Lỗi: Số điện thoại và CCCD không được bỏ trống!")
                return
                
            try:
                so_ngay = int(input("Nhập số ngày ở: "))
                if so_ngay <= 0:
                    print("Lỗi: Số ngày ở không hợp lệ (phải lớn hơn 0)!")
                    return
                
                p["khach_hang"] = {
                    "ma_kh": ma_kh,
                    "ho_ten": ho_ten,
                    "sdt": sdt,
                    "cccd": cccd,
                    "so_ngay": so_ngay
                }
                p["trang_thai"] = "Đang sử dụng"
                luu_du_lieu()
                print("Đặt phòng thành công!")
            except ValueError:
                print("Lỗi: Số ngày ở phải là số nguyên!")
            return
            
    print("Lỗi: Không tìm thấy mã phòng!")

def tra_phong():
    global doanh_thu_tong
    doc_du_lieu()
    ma_phong = input("Nhập mã phòng muốn trả: ").strip()
    for p in danh_sach_phong:
        if p["ma_phong"] == ma_phong:
            if p["trang_thai"] == "Trống":
                print("Lỗi: Phòng này hiện đang trống, không thể trả!")
                return
            
            kh = p["khach_hang"]
            tien_phong = p["gia_phong"] * kh["so_ngay"]
            doanh_thu_tong += tien_phong
            
            print("\n" + "="*40)
            print("         HÓA ĐƠN TRẢ PHÒNG")
            print("="*40)
            print(f"Mã phòng: {p['ma_phong']}   | Số phòng: {p['so_phong']}")
            print(f"Khách hàng: {kh['ho_ten']} (Mã KH: {kh['ma_kh']})")
            print(f"Số ngày ở: {kh['so_ngay']} ngày")
            print(f"Đơn giá: {p['gia_phong']:,.0f} VNĐ/ngày")
            print("-" * 40)
            print(f"Tổng tiền thanh toán: {tien_phong:,.0f} VNĐ")
            print("="*40)
            
            p["trang_thai"] = "Trống"
            p["khach_hang"] = {}
            luu_du_lieu()
            print("Đã trả phòng và cập nhật trạng thái thành công!")
            return
            
    print("Lỗi: Không tìm thấy mã phòng!")

def thong_ke():
    tong_phong = len(danh_sach_phong)
    if tong_phong == 0:
        print("Hiện chưa có phòng nào trong hệ thống.")
        return
        
    phong_trong = sum(1 for p in danh_sach_phong if p["trang_thai"] == "Trống")
    phong_dang_su_dung = tong_phong - phong_trong
    
    dem_loai_phong = {}
    for p in danh_sach_phong:
        if p["trang_thai"] == "Đang sử dụng":
            loai = p["loai_phong"]
            dem_loai_phong[loai] = dem_loai_phong.get(loai, 0) + 1
            
    if dem_loai_phong:
        loai_pho_bien = max(dem_loai_phong, key=dem_loai_phong.get)
    else:
        loai_pho_bien = "Không có (chưa có khách thuê)"

    print("\n" + "="*40)
    print("             BẢNG THỐNG KÊ")
    print("="*40)
    print(f"Tổng số phòng: {tong_phong}")
    print(f"Số phòng trống: {phong_trong}")
    print(f"Số phòng đang sử dụng: {phong_dang_su_dung}")
    print(f"Loại phòng đang sử dụng nhiều nhất: {loai_pho_bien}")
    print(f"Tổng doanh thu hệ thống: {doanh_thu_tong:,.0f} VNĐ")
    print("="*40)

def doc_du_lieu_menu():
    global danh_sach_phong, doanh_thu_tong
    try:
        with open(TEN_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            danh_sach_phong = data.get("danh_sach_phong", [])
            doanh_thu_tong = data.get("doanh_thu_tong", 0.0)
        print("Đọc dữ liệu từ file data.txt thành công!")
    except FileNotFoundError:
        print("Lỗi: Không tìm thấy file dữ liệu (data.txt)!")
    except Exception as e:
        print(f"Lỗi đọc file: {e}")

def main():
    # Tự động nạp dữ liệu từ file khi khởi động nếu file đã tồn tại
    doc_du_lieu()
    
    while True:
        print("\n" + "="*40)
        print("          QUẢN LÝ KHÁCH SẠN")
        print("="*40)
        print("1. Thêm phòng")
        print("2. Hiển thị phòng")
        print("3. Cập nhật phòng")
        print("4. Xóa phòng")
        print("5. Tìm kiếm")
        print("6. Sắp xếp")
        print("7. Đặt phòng")
        print("8. Trả phòng")
        print("9. Thống kê")
        print("10. Lưu dữ liệu")
        print("11. Đọc dữ liệu")
        print("0. Thoát")
        print("="*40)
        
        chon = input("Lựa chọn: ").strip()
        
        if chon == '1':
            them_phong()
        elif chon == '2':
            hien_thi_phong()
        elif chon == '3':
            cap_nhat_phong()
        elif chon == '4':
            xoa_phong()
        elif chon == '5':
            tim_kiem()
        elif chon == '6':
            sap_xep()
        elif chon == '7':
            dat_phong()
        elif chon == '8':
            tra_phong()
        elif chon == '9':
            thong_ke()
        elif chon == '10':
            luu_du_lieu()
        elif chon == '11':
            doc_du_lieu_menu()
        elif chon == '0':
            print("Đã thoát chương trình. Hẹn gặp lại!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại!")

if __name__ == "__main__":
    main()