import numpy as np
import cv2


class PointList():
    def __init__(self, npoints):
        self.npoints = npoints
        self.ptlist = np.empty((npoints, 2), dtype=int)
        self.pos = 0

    def add(self, x, y):
        if self.pos < self.npoints:
            self.ptlist[self.pos, :] = [x, y]
            self.pos += 1
            return True
        return False


def onMouse(event, x, y, flag, params):
    wname, img, ptlist = params
    if event == cv2.EVENT_MOUSEMOVE:  # マウスが移動したときにx線とy線を更新する
        if ptlist.pos == 1:
            img3 = np.copy(img)
            x_list = [x, ptlist.ptlist[0][0]]
            x_list.sort()
            y_list = [y, ptlist.ptlist[0][1]]
            y_list.sort()
            cv2.rectangle(img3,
                          (x_list[0], y_list[1]),
                          (x_list[1], y_list[0]),
                          color=(255, 255, 0),
                          thickness=1)
            cv2.imshow(wname, img3)
        else:
            img2 = np.copy(img)
            h, w = img2.shape[0], img2.shape[1]
            cv2.line(img2, (x, 0), (x, h - 1), (255, 0, 0))
            cv2.line(img2, (0, y), (w - 1, y), (255, 0, 0))
            cv2.imshow(wname, img2)

    if event == cv2.EVENT_LBUTTONDOWN:  # レフトボタンをクリックしたとき、ptlist配列にx,y座標を格納する
        if ptlist.add(x, y):
            print('[%d] ( %d, %d )' % (ptlist.pos - 1, x, y))
            cv2.circle(img, (x, y), 3, (0, 0, 255), 3)
            cv2.imshow(wname, img)
        else:
            print('All points have selected.  Press ESC-key.')
        if ptlist.pos == ptlist.npoints:
            cv2.rectangle(img,
                          (np.min(ptlist.ptlist, axis=0)[0],
                           np.max(ptlist.ptlist, axis=0)[1]),
                          (np.max(ptlist.ptlist, axis=0)[0],
                           np.min(ptlist.ptlist, axis=0)[1]),
                          color=(0, 255, 0),
                          thickness=2)

if __name__ == '__main__':
    img = cv2.imread("/Users/kwhtsng/coo_cap/data/000007.jpg")
    wname = "MouseEvent"
    cv2.namedWindow(wname)
    npoints = 2
    ptlist = PointList(npoints)
    cv2.setMouseCallback(wname, onMouse, [wname, img, ptlist])
    cv2.imshow(wname, img)
    cv2.waitKey()
    cv2.destroyAllWindows()

