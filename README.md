# 🚌 Dự án Phát Sinh Nhu Cầu Đi Lại (MATSim Demand Generator)

Chào mừng! Đây là bộ công cụ giúp bạn tạo ra file `plan.xml` cho mô phỏng MATSim một cách tự động. 

Tài liệu này được thiết kế theo dạng **Quy trình từng bước (Step-by-Step Flow)** để người mới bắt đầu có thể áp dụng ngay lập tức.

---

> 🚨 **CẢNH BÁO QUAN TRỌNG NHẤT: ĐƠN VỊ TÍNH** 🚨
>
> Trước khi làm bất cứ điều gì, hãy khắc cốt ghi tâm điều này:
> Trong toàn bộ dự án (đặc biệt là file `config_scenario.yaml`), **TẤT CẢ** các đơn vị đo lường khoảng cách và tọa độ đều là **KILOMET (KM)**.
>
> *   ✅ `x: 10`, `y: 20` $\rightarrow$ Tọa độ (10km, 20km).
> *   ✅ `radius: 1.5` $\rightarrow$ Bán kính 1.5 km.
> *   ❌ **SAI LẦM PHỔ BIẾN**: Nhập `radius: 1000` (ý là 1000m) $\rightarrow$ Máy tính sẽ hiểu là bán kính **1000 KM** (to bằng cả một quốc gia)!

---

## 👣 QUY TRÌNH THỰC HIỆN CHUẨN (4 BƯỚC)

Để chạy dự án thành công, bạn hãy đi theo đúng 4 bước tuần tự dưới đây:

### 🟢 Bước 1: Cài đặt môi trường (Setup)
Bạn chỉ cần làm bước này một lần duy nhất khi mới tải code về.

1.  **Cài Python**: Đảm bảo máy có [Python 3.10+](https://www.python.org/downloads/). Kiểm tra bằng lệnh `python --version` trong Terminal (hoặc CMD).
2.  **Cài thư viện**: Tại thư mục chứa file này, chạy lệnh:
    ```bash
    pip install -r requirements.txt
    ```

### 🟡 Bước 2: Cấu hình kịch bản (Configuration)
Đây là bước bạn sẽ làm việc nhiều nhất. Hãy mở file **`config/config_scenario.yaml`**.

#### 2.1. Cấu hình Thời gian (`peakhours`)
Quyết định giờ cao điểm mà mọi người sẽ đổ ra đường.
```yaml
peakhours:
  am: 
    hour: [9, 10] # Giờ cao điểm sáng (tập trung lúc 9h và 10h)
  pm: 
    hour: [17]    # Giờ cao điểm chiều (tập trung lúc 17h)
```

#### 2.2. Cấu hình Không gian (`hotspots` & `workspots`)
Chúng ta sử dụng tư duy **"Vùng mẹ - Điểm con"** để tạo dữ liệu sinh động.

*   **Vùng mẹ (Region)**: Là một khu vực lớn (Ví dụ: Quận Cầu Giấy). Được định nghĩa bằng tâm (`center_region`) và bán kính (`radius_region`).
*   **Điểm con (Subregions)**: Máy tính sẽ chọn ngẫu nhiên các điểm tụ bên trong Vùng mẹ để làm các xóm dân cư, thay vì rải đều tăm tắp.

```yaml
hotspots_region:
  - prefix_region_id: "Q1"      # Tên vùng
    object_type: "hotspot"      # Loại: Nhà (hotspot)
    subregions_number: 10       # Tạo ra 10 'xóm' dân cư trong vùng này
    region_type: "circle"       # Hình tròn
    center_region: {x: 5, y: 10} # Tọa độ tâm (KM)
    radius_region: 2            # Bán kính 2 KM (Nhớ chú ý đơn vị!)
    population_number: 5000     # Tổng 5000 dân chia cho 10 xóm
```

### 🟠 Bước 3: Chạy mô phỏng (Execution)
Sau khi đã lưu file config, bạn chạy lệnh sau để sinh dữ liệu.

📍 **Cách chạy đúng:**
Mở Terminal tại thư mục gốc dự án (nơi chứa file README này) và gõ:

```bash
python -m src.Main
```

> ⚠️ **Lưu ý:** Tuyệt đối không chạy kiểu `python src/Main.py` (sẽ lỗi import).

### 🔴 Bước 4: Kiểm tra kết quả (Output)
Nếu chạy thành công, dữ liệu sẽ nằm trong thư mục **`data/processed/`**:

1.  **`plan.xml`**: 🔥 **Quan trọng nhất**. Đây là file chứa toàn bộ lịch trình đi lại của dân cư. Bạn dùng file này để nạp vào MATSim.
2.  **`OD.csv`**: File Excel thống kê nhu cầu đi lại (Từ vùng nào -> Đến vùng nào, số lượng bao nhiêu). Dùng để vẽ biểu đồ báo cáo.
3.  **`spot.csv`**: Chứa tọa độ chính xác của các Hotspot/Workspot đã tạo. Bạn nên mở file này lên (hoặc import vào QGIS/Google Earth) để kiểm tra xem vị trí có đúng ý đồ không.

---

## 🧠 LUỒNG XỬ LÝ DỮ LIỆU (LOGIC FLOW)

Nếu bạn muốn hiểu code chạy ngầm như thế nào, đây là sơ đồ tư duy:

```mermaid
graph TD
    Start[Bắt đầu] --> LoadConfig[1. Đọc Config (File .yaml)]
    
    subgraph Giai_doan_1_Sinh_Khong_Gian
    LoadConfig --> Region[Tạo Vùng Mẹ]
    Region --> SubRegion[Sinh ngẫu nhiên các Điểm Con (Xóm/Tòa nhà)]
    SubRegion --> Pop[Rải dân số vào các Hotspot]
    end
    
    subgraph Giai_doan_2_Ghep_Cap [Logic Quan Trọng Nhất]
    Pop --> CalAttr[Tính độ hấp dẫn của Workspot]
    CalAttr --> Gravity[2. Chạy Mô Hình Trọng Lực]
    Gravity --> Match[Ghép Người -> Nơi làm phù hợp]
    end
    
    subgraph Giai_doan_3_Lap_Lich
    Match --> Time[3. Gán giờ xuất phát (theo Peak Hours)]
    Time --> Plan[Tạo hành trình: Nhà -> Chỗ làm -> Nhà]
    end
    
    Plan --> Output[4. Xuất file plan.xml & OD.csv]
```

**Giải thích logic "Ghép cặp":**
Khi một người dân chọn nơi làm việc, họ sẽ cân nhắc 2 yếu tố:
1.  **Khoảng cách**: Ưu tiên nơi gần nhà (nghịch đảo khoảng cách).
2.  **Độ hấp dẫn**: Ưu tiên nơi sầm uất, gần các khu dân cư đông đúc khác.
$\rightarrow$ Đây chính là bản chất của **Mô hình Trọng lực (Gravity Model)** được áp dụng trong code.

---

## ❓ Xử lý sự cố thường gặp

*   **Lỗi**: `ModuleNotFoundError: No module named 'src'`
    *   👉 **Sửa**: Bạn đang chạy sai lệnh. Hãy dùng `python -m src.Main`.
*   **Vấn đề**: File output trống trơn hoặc tọa độ lạ?
    *   👉 **Sửa**: Kiểm tra lại đơn vị trong config. Có thể bạn đã nhập mét thay vì KM.