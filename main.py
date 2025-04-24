from shared.data_loader import load_data

# جرب تحميل ملف معين
roads_df = load_data("roads")

# اعرض أول 5 صفوف للتأكد
print(roads_df.head())
