import createImage
import detectDifference

if __name__ == '__main__':
    path = './Image/image2.jpg'
    level = 'medium'
    limit = 10
    createImage.CreateImage(path, level, limit)
    detectDifference.DetectDifference()

