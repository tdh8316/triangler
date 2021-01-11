from tkinter import filedialog, Tk

import triangler
from triangler import EdgeMethod, SampleMethod, ColorMethod

Tk().withdraw()
img_path = str(filedialog.askopenfilename(title="사진을 선택해 주세요.",
                                          filetypes=(("사진 파일", "*.jpg;*.png"), ("모든 파일", "*.*"),)))
print(img_path)
# Create Triangler instance
t = triangler.Triangler(
    edge_method=EdgeMethod[(input("엣지 검출 {canny|sobel|entropy} [기본값:sobel]=") or "sobel").upper()],
    sample_method=SampleMethod[
        (input("샘플링 알고리즘 {poisson_disk|threshold} [기본값:poisson_disk]=") or "poisson_disk").upper()],
    color_method=ColorMethod[(input("색상 배합 {centroid|mean} [기본값:centroid]=") or "centroid").upper()],
    points=int(input("점의 개수 [기본값:1000]=") or 1000),
)

t.save(img_path, print_log=True)

input("완료되었습니다!")
