package main

import (
	"flag"
	"fmt"
	"os"
)

var (
	start    int
	end      int
	filePath string
	rev      bool
	d        map[State]bool
)

var INIT = 61

type State = [9]byte

type Operator struct {
	mapping map[[2]byte]byte
}

func NewOperator(tt, tm, tf, mt, mm, mf, ft, fm, ff byte) Operator {
	return Operator{
		mapping: map[[2]byte]byte{
			{2, 2}: tt,
			{2, 1}: tm,
			{2, 0}: tf,
			{1, 2}: mt,
			{1, 1}: mm,
			{1, 0}: mf,
			{0, 2}: ft,
			{0, 1}: fm,
			{0, 0}: ff,
		},
	}
}

func (op Operator) cal(formmar, latter State) State {
	s := State{}
	for i := 0; i < 9; i++ {
		s[i] = op.mapping[[2]byte{formmar[i], latter[i]}]
	}
	return s
}

func check(op Operator, f *os.File, d map[State]bool) {
	s1 := State{2, 2, 2, 1, 1, 1, 0, 0, 0}
	s2 := State{2, 1, 0, 2, 1, 0, 2, 1, 0}
	d[s1] = true
	d[s2] = true
	que := []State{s1, s2}
	for len(que) != 0 {
		s := que[0]
		new := make(map[State]bool, 3)
		que = que[1:]
		res := op.cal(s, s)
		if _, ok := d[res]; !ok {
			new[res] = true
		}
		for v := range d {
			res = op.cal(s, v)
			if _, ok := d[res]; !ok {
				new[res] = true
			}
			res = op.cal(v, s)
			if _, ok := d[res]; !ok {
				new[res] = true
			}
		}
		for v := range new {
			d[v] = true
			que = append(que, v)
		}
	}
	f.WriteString(fmt.Sprintf("%d |", op.mapping))
	f.WriteString(fmt.Sprintln(len(d)))
	for i := range d {
		delete(d, i)
	}
}

func full_arrangement() (res []State) {
	for i1 := byte(0); i1 < 3; i1++ {
		for i2 := byte(0); i2 < 3; i2++ {
			for i3 := byte(0); i3 < 3; i3++ {
				for i4 := byte(0); i4 < 3; i4++ {
					for i5 := byte(0); i5 < 3; i5++ {
						for i6 := byte(0); i6 < 3; i6++ {
							for i7 := byte(0); i7 < 3; i7++ {
								for i8 := byte(0); i8 < 3; i8++ {
									for i9 := byte(0); i9 < 3; i9++ {
										res = append(res, State{i1, i2, i3, i4, i5, i6, i7, i8, i9})
									}
								}
							}
						}
					}
				}
			}
		}
	}
	return
}

func getFlag() {
	flag.IntVar(&start, "s", 0, "")
	flag.IntVar(&end, "e", 19683, "")
	flag.StringVar(&filePath, "p", "./output", "")
	flag.BoolVar(&rev, "rev", false, "")
	flag.Parse()
}

func main() {
	d = make(map[State]bool, 19683)
	getFlag()
	idx := start
	file, err := os.OpenFile(filePath, os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		panic(err)
	}
	defer file.Close()
	arrangements := full_arrangement()
	if rev {
		for i, j := 0, len(arrangements); i < j; {
			arrangements[i], arrangements[j] = arrangements[j], arrangements[i]
			i++
			j--
		}

	}
	for _, v := range full_arrangement()[start:end] {
		file.WriteString(fmt.Sprintf("%d / %d |", idx, 19683))
		check(NewOperator(v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8]), file, d)
		idx++
	}
}
