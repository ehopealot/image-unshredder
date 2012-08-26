from PIL import Image

SHRED_WIDTH = 32
NUMBER_SHREDS = 20

class Region(object):
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def __unicode__(self):
        return "({0},{1},{2},{3})".format(self.x1,self.x2,self.x3,self.x4)

class Shred(object):
    def __init__(self, image, region, id):
        self.id = id
        self.image = image
        self.region = region
        self.data = self.image.getdata()
        self.left_edge, self.right_edge = self.get_edge_data()
        self.left_scores, self.right_scores = {}, {}

    def get_edge_data(self):
        left, right = [],[]
        current = left
        for x in (self.region.x1, self.region.x2-1):
            for y in range(self.region.y1, self.region.y2):
                current.append(self.get_pixel_value(x, y))
            current = right
        return left, right   

    def get_pixel_value(self, x, y):
        width, height = self.image.size
        # Go y rows down and then x pixels over
        pixel = self.data[y * width + x]
        return pixel        

    def get_grayscale(self, red, green, blue, alpha):
        return .11*blue + .59*green + .30 * red

    def compare(self, my_edge, other_edge):
        score = 0
        for index, pixel in enumerate(my_edge):
            other_pixel = other_edge[index]
            my_pixel_gray = self.get_grayscale(*pixel)
            other_pixel_gray = self.get_grayscale(*other_pixel)
            pixels = zip(pixel, other_pixel)
            similar = True
            for index, value in enumerate(pixel):
                if abs(value - other_pixel[index]) > 10:
                    similar = False
                    break
            score += 1 if similar else 0
                

        return score

    def compare_left(self, other_shred):
        return self.compare(self.left_edge, other_shred.right_edge)

    def compare_right(self, other_shred):
        return self.compare(self.right_edge, other_shred.left_edge)

    def closest_left_score(self):
        return max(self.left_scores.items(),key=lambda item:item[0])

    def next_closest_right_score(self):
        return sorted(self.right_scores.items(), key=lambda item:item[0])[1]

    def closest_right_score(self):
        return max(self.right_scores.items(), key=lambda item:item[0])

    def total_left_similarity(self):
        return sum(self.left_scores.keys())

    def total_right_similarity(self):
        return sum(self.right_scores.keys())

class Unshredder(object):
    def __init__(self, image_name):
        self.image = Image.open(image_name)
        self.data = self.image.getdata()
        self.shreds = []                       
        x1, y1, x2, y2 = 0, 0, SHRED_WIDTH, self.image.size[1]
        for i in range(NUMBER_SHREDS):
            region = Region(x1, y1, x2, y2)
            self.shreds.append(Shred(self.image, region, i))
            x1 += SHRED_WIDTH
            x2 += SHRED_WIDTH
    
    def solve(self):
        for index, shred in enumerate(self.shreds):
            for shred2 in self.shreds[index+1:]:
                left_score = shred.compare_left(shred2)
                right_score = shred.compare_right(shred2)
                shred.left_scores[left_score] = shred2
                shred.right_scores[right_score] = shred2
                shred2.left_scores[right_score] = shred
                shred2.right_scores[left_score] = shred
        left = min(self.shreds, key=lambda shred:shred.closest_left_score()[0])
        right = min(self.shreds, key=lambda shred:shred.closest_right_score()[0])
        unshredded = Image.new("RGBA", self.image.size)
        x1, y1, x2, y2 = left.id*SHRED_WIDTH, 0, left.id*SHRED_WIDTH+SHRED_WIDTH, self.image.size[1]
        source_region = self.image.crop((x1,y1,x2,y2))
        destination_point = (0,0)
        unshredded.paste(source_region, destination_point)
        shreds_pasted = 1
        last_shred = left
        while shreds_pasted < NUMBER_SHREDS:
            next_shred = last_shred.closest_right_score()[1]
            x1 = next_shred.id * SHRED_WIDTH
            x2 += x1 + SHRED_WIDTH
            destination_point = (destination_point[0]+SHRED_WIDTH, 0)
            source_region = self.image.crop((x1, y1, x2, y2))
            unshredded.paste(source_region, destination_point)
            last_shred = next_shred
            shreds_pasted += 1
        
        unshredded.save("unshredded.jpg", "JPEG")

def run():
    unshredder = Unshredder('TokyoPanoramaShredded.png')
    unshredder.solve()
    




if __name__ == "__main__":
    run()
