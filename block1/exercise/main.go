package main

import(
	"image"
	"image/color"
	"image/draw"
	_ "image/jpeg"
	"image/png"
	"os"
	"math"
)

func readImage(path string) (*image.NRGBA, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	img, _, err := image.Decode(f)
	nrgba := image.NewNRGBA(img.Bounds())
	draw.Draw(nrgba, nrgba.Bounds(), img, img.Bounds().Min, draw.Src)
	return nrgba, err
}

func writeImage(path string, img image.Image) error {
	f, err := os.Create(path)
	if err != nil {
		return err
	}
	defer f.Close()
	return png.Encode(f, img)
}

type Kernel struct {
	Modifiers []float64
	Width, Height int
}

func (k *Kernel) GetModifier(x, y int) float64 {
	return k.Modifiers[x + y * k.Width]
}

func (k *Kernel) EvalPixel(in *image.NRGBA, x, y int) color.RGBA {
	rSum, gSum, bSum := 0.0, 0.0, 0.0
	halfWidth := k.Width / 2
	halfHeight := k.Height / 2

	pt := in.Bounds().Max
	w, h := pt.X, pt.Y

	for i := -halfWidth; i <= halfWidth; i++ {
		for j := -halfHeight; j <= halfHeight; j++ {
			iX, iY := i + x, j + y
			if iX >= 0 && iX < w && iY >= 0 && iY < h {
				clr := in.NRGBAAt(iX, iY)
				r, g, b := clr.R, clr.G, clr.B
				mod := k.GetModifier(i + halfWidth, j + halfHeight)
				rSum += (mod * float64(r))
				gSum += (mod * float64(g))
				bSum += (mod * float64(b))
			}
		}
	}

	return color.RGBA{
		uint8(Round(rSum)),
		uint8(Round(gSum)),
		uint8(Round(bSum)),
		255,
	}
}

func Round(f float64) int {
	return int(math.Round(f))
}

func (k *Kernel) Apply(in *image.NRGBA) *image.NRGBA {
	out := image.NewNRGBA(in.Bounds())
	pt := out.Bounds().Max
	w, h := pt.X, pt.Y

	for x := 0; x < w; x++ {
		for y := 0; y < h; y++ {
			pixel := k.EvalPixel(in, x, y)
			out.Set(x, y, pixel)
		}
	}

	return out
}

func main() {
	img, err := readImage("let_it_bee.jpg")
	if err != nil {
		panic(err)
	}

	/*
	//c := 1.0/9.0
	k := Kernel{
		Modifiers: []float64{
			c, c, c,
			c, c, c,
			c, c, c,
		},
		Width: 3,
		Height: 3,
	}
	*/

	/*
	c2 := 1.0/25.0
	k := Kernel{
		Modifiers: []float64{
			c2, c2, c2, c2, c2,
			c2, c2, c2, c2, c2,
			c2, c2, c2, c2, c2,
			c2, c2, c2, c2, c2,
			c2, c2, c2, c2, c2,
		},
		Width: 5,
		Height: 5,
	}
	*/

	k := Kernel{
		Modifiers: []float64{
			 0, -1,  0,
			-1,  5, -1,
			 0, -1,  0,
		},
		Width: 3,
		Height: 3,
	}

	/*
	// Den här ballar ur delux, sum(Modifiers) > 1
	k := Kernel{
		Modifiers: []float64{
			0.0652, 0.25, 0.0652,
			0.25,  0.25,  0.25,
			0.0652, 0.25, 0.0652,
		},
		Width: 3,
		Height: 3,
	}
	*/

	/*
	// Gausian 7x7
	k := Kernel{
		Modifiers: []float64{
			0.00000067, 0.00002292, 0.00019117, 0.00038771, 0.00019117, 0.00002292, 0.00000067,
			0.00002292, 0.00078633, 0.00655965, 0.01330373, 0.00655965, 0.00078633, 0.00002292,
			0.00019117, 0.00655965, 0.05472157, 0.11098164, 0.05472157, 0.00655965, 0.00019117,
			0.00039771, 0.01330373, 0.11098164, 0.22508352, 0.11098164, 0.01330373, 0.00039771,
			0.00019117, 0.00655965, 0.05472157, 0.11098164, 0.05472157, 0.00655965, 0.00019117,
			0.00002292, 0.00078633, 0.00655965, 0.01330373, 0.00655965, 0.00078633, 0.00002292,
			0.00000067, 0.00002292, 0.00019117, 0.00038771, 0.00019117, 0.00002292, 0.00000067,
		},
		Width: 7,
		Height: 7,
	}
	*/

	out := k.Apply(img)

	/*
	// Vroom vroom
	for i:= 0; i < 20; i++ {
		out = k.Apply(out)
	}
	*/

	err = writeImage("let_it_sharpen.png", out)
	if err != nil {
		panic(err)
	}
}
