import os
import sys
import glob
import xml.etree.ElementTree as et
import xml.dom.minidom as md
import numpy as np
import cv2


def mkXml(folder, filename, path, size, names,
        bndboxes, database="Unknown", segmented=0,
        pose="Unspecified", truncated=0, difficult=0
        ):

    a             = et.Element("annotation")
    tree          = et.ElementTree(element=a)

    a_folder      = et.SubElement(a, "folder")
    a_folder.text = str(folder)

    a_file        = et.SubElement(a, "filename")
    a_file.text   = str(filename)

    a_path        = et.SubElement(a, "path")
    a_path.text   = str(path)

    a_size        = et.SubElement(a, "size")
    size_w        = et.SubElement(a_size, "width")
    size_w.text   = str(size[0])
    size_h        = et.SubElement(a_size, "height")
    size_h.text   = str(size[1])
    size_d        = et.SubElement(a_size, "depth")
    size_d.text   = str(size[2])

    a_seg         = et.SubElement(a, "segmented")
    a_seg.text    = str(segmented)

    for i, name in enumerate(names):
        a_object              = et.SubElement(a, "object")

        object_name           = et.SubElement(a_object, "name")
        object_name.text      = str(name)

        object_pose           = et.SubElement(a_object, "pose")
        object_pose.text      = str(pose)

        object_truncated      = et.SubElement(a_object, "truncated")
        object_truncated.text = str(truncated)

        object_difficult      = et.SubElement(a_object, "difficult")
        object_difficult.text = str(difficult)

        object_bndbox         = et.SubElement(a_object, "bndbox")

        bndbox_xmin           = et.SubElement(object_bndbox, "xmin")
        bndbox_xmin.text      = str(bndboxes[i][0])

        bndbox_ymin           = et.SubElement(object_bndbox, "ymin")
        bndbox_ymin.text      = str(bndboxes[i][1])

        bndbox_xmax           = et.SubElement(object_bndbox, "xmax")
        bndbox_xmax.text      = str(bndboxes[i][2])

        bndbox_ymax           = et.SubElement(object_bndbox, "ymax")
        bndbox_ymax.text      = str(bndboxes[i][3])

    # 文字列パースを介してminidomへ移す
    document = md.parseString(et.tostring(a, 'utf-8'))

    f = "xml/" + filename + ".xml"

    f = open(f, "w")
    document.writexml(f,
                encoding="utf-8",
                newl='\n',
                indent='',
                addindent='    ')
    f.close()

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
                          (x_list[0], y_list[0]),
                          (x_list[1], y_list[1]),
                          color=(0, 255, 255),
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
            cv2.circle(img, (x, y), 3, (0, 0, 255), 3)
            cv2.imshow(wname, img)
        else:
            print('これ以上選択できません。各キーで操作を行ってください。')
        if ptlist.pos == 2:
            global upper_left
            global lower_right
            upper_left = [np.min(ptlist.ptlist, axis=0)[0], np.min(ptlist.ptlist, axis=0)[1]]
            lower_right = [np.max(ptlist.ptlist, axis=0)[0], np.max(ptlist.ptlist, axis=0)[1]]
            cv2.rectangle(img,
                          (upper_left[0], upper_left[1]),
                          (lower_right[0], lower_right[1]),
                          color=(0, 255, 0),
                          thickness=1)

if __name__ == '__main__':
    os.makedirs("data", exist_ok = True)
    os.makedirs("xml",  exist_ok = True)

    files = glob.glob("data/*.jpg")

    if not files:
        exit("画像がありませんでした。")
    files.sort()

    last_file = []
    i         = 0

    print("以下の操作を繰り返し、画像内のオブジェクトを選択してください。\n"
          "    1. マウスを使ってオブジェクトを四角で囲む。\n"
          "    2. A キーで確定、オブジェクト名を選択。\n")
    print("その他操作\n"
          "    N => 何もせず次の画像へ\n"
          "    B => 何もせず前の画像へ\n"
          "    C => 範囲選択のやりなおし\n"
          "    Q => プログラムの終了\n")

    while(i < len(files)):
        files[i] = os.path.abspath(files[i])
        names    = []
        bndboxs  = []

        while(True):
            filename, ext = os.path.splitext(os.path.basename(files[i]))
            img           = cv2.imread(files[i])
            wname         = files[i]
            cv2.namedWindow(wname)
            npoints       = 2
            ptlist        = PointList(npoints)
            key           = ""

            while(not key):
                cv2.setMouseCallback(wname, onMouse, [wname, img, ptlist])
                cv2.imshow(wname, img)
                key = cv2.waitKey(0) & 0xFF

            if key == ord("q"):
                cv2.destroyAllWindows()
                exit("終了します。\n")

            elif key == ord("a"):
                print("オブジェクトを、各キーで選択してください。\n"
                      "    C => ウオノエ\n"
                      "    Q => 入力をキャンセル\n")

                key2 = ""

                while(not key2):
                    key2 = cv2.waitKey(0) & 0xFF

                if key2 == ord("q"):
                    print("入力をキャンセルしました。\n")

                elif key2 == ord("c"):
                    names.append("Cymothoidae")
                    bndboxs.append([upper_left[0],
                                    upper_left[1],
                                   lower_right[0],
                                   lower_right[1]])
                    print("オブジェクトを追加しました。")
                    print("    オブジェクト名 => {}\n    座標 => (x min => {}, y min => {}, x max => {}, y max => {})\n".format(names[-1], bndboxs[-1][0], bndboxs[-1][1], bndboxs[-1][2], bndboxs[-1][3]))
                    print("オブジェクトを全て選び終えた場合、X キーによって出力、次の画像へ。\n")
                    continue

            elif key == ord("x"):
                if not names:
                    print("少なくともひとつ、オブジェクト名を入力してください。\n")
                    continue

                print("xmlファイルを出力しました。\n"
                      "    ファイル名 => '" + filename + ".xml'\n")
                mkXml("data", filename, files[i],
                      [640, 480, 3], names, bndboxs)
                i += 1

            elif key == ord("c"):
                print("座標指定をやり直します。\n")
                continue

            elif key == ord("n"):
                print("次の画像に進みました。\n")
                i += 1

            elif key == ord("b"):
                print("前の画像に戻りました。\n")
                if i == 0:
                    print("これ以上戻れません。\n")
                else:
                    i -= 1

            cv2.destroyAllWindows()
            break

    print("全ての画像の座標登録が終わりました。\n")
