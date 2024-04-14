#include <iostream>
#include <immintrin.h>

typedef uint64_t Bit;
typedef uint64_t Square;
typedef uint64_t map;

#define SquareOf(X) _txcnt_u64(X)
#define Bitloop(X) for(;X; X = _blsr_u64(X))

inline static Bit PopBit(uint64_t &val) {
    uint64_t lsb = _blsi_u64(val);
    val ^= lsb;
    return lsb;
}

class BoardStatus {
    static constexpr uint64_t WNotOccupiedL = 0b01110000ull;
    static constexpr uint64_t WNotAttackedL = 0b00111000ull;

    static constexpr uint64_t WNotOccupiedR = 0b00000110ull;
    static constexpr uint64_t WNotAttackedR = 0b00001110ull;

    static constexpr uint64_t BNotOccupiedL = 0b01110000ull << 56ull;
    static constexpr uint64_t BNotAttackedL = 0b00111000ull << 56ull;

    static constexpr uint64_t BNotOccupiedR = 0b00000110ull << 56ull;
    static constexpr uint64_t BNotAttackedR = 0b00001110ull << 56ull;

    static constexpr uint64_t WRookL_Change = 0b11111000ull;
    static constexpr uint64_t BRookL_Change = 0b11111000ull << 56ull;
    static constexpr uint64_t WRookR_Change = 0b00001111ull;
    static constexpr uint64_t BRookR_Change = 0b00001111ull << 56ull;

    static constexpr uint64_t WRookL = 0b10000000ull;
    static constexpr uint64_t BRookL = 0b10000000ull << 56ull;
    static constexpr uint64_t WRookR = 0b00000001ull;
    static constexpr uint64_t BRookR = 0b00000001ull << 56ull;
public:
    const bool WhiteMove;
    const bool HasEPPawn;
    const bool WCastleL;
    const bool WCastleR;
    const bool BCastleL;
    const bool BCastleR;

    constexpr BoardStatus(bool white, bool ep, bool wcast_left, bool wcast_right, bool bcast_left, bool bcast_right) :
        WhiteMove(white), HasEPPawn(ep), WCastleL(wcast_left), WCastleR(wcast_right), BCastleL(bcast_left), BCastleR(bcast_right) 
    {

    }
    
    constexpr BoardStatus(int pat) :
        WhiteMove((pat & 0b100000) != 0), HasEPPawn((pat & 0b010000) != 0), 
        WCastleL((pat & 0b001000) != 0), WCastleR((pat & 0b000100) != 0), 
        BCastleL((pat & 0b000010) != 0), BCastleR((pat & 0b000001) != 0)
    {

    }

    constexpr bool CanCastle() const {
        if (WhiteMove) return WCastleL | WCastleR;
        else return BCastleL | BCastleR;
    }

    constexpr bool CanCastleLeft() const {
        if (WhiteMove) return WCastleL;
        else return BCastleL;
    }

    constexpr bool CanCastleRight() const {
        if (WhiteMove) return WCastleR;
        else return BCastleR;
    }

    // Return if Castling Left is an option
    inline constexpr bool CanCastleLeft(map attacked, map occupied, map rook) const {
        if (WhiteMove && WCastleL) {
            if (occupied & WNotOccupiedL) return false;
            if (attacked & WNotAttackedL) return false;
            if (rook & BRookL) return true;
            return false;
        }
        else if (BCastleL) {
            if (occupied & BNotOccupiedL) return false;
            if (attacked & BNotAttackedL) return false;
            if (rook & BRookL) return true;
            return false;
        }
        return false;
    }

    // Return if Castling Right is an option
    inline constexpr bool CanCastleRight(map attacked, map occupied, map rook) const {
        if (WhiteMove && WCastleR) {
            if (occupied & WNotOccupiedR) return false;
            if (attacked & WNotAttackedR) return false;
            if (rook & WRookR) return true;
            return false;
        }
        else if (BCastleR) {
            if (occupied & BNotOccupiedR) return false;
            if (attacked & BNotAttackedR) return false;
            if (rook & BRookR) return true;
            return false;
        }
        return false;
    }

    constexpr bool IsLeftRook(Bit rook) const {
        if (WhiteMove) return WRookL == rook;
        else return BRookL == rook;
    }
    constexpr bool IsRightRook(Bit rook) const {
        if (WhiteMove) return WRookR == rook;
        else return BRookR == rook;
    }

    static constexpr BoardStatus Default() {
        // white, no ep, not in check , all castling rights
        return BoardStatus(true, false, true, true, true, true);
    }

    constexpr BoardStatus PawnPush() const {
        return BoardStatus(!WhiteMove, true, WCastleL, WCastleR, BCastleL, BCastleR);
    }

    //Moving the king
    constexpr BoardStatus KingMove() const {
        if (WhiteMove) {
            return BoardStatus(!WhiteMove, false, false, false, BCastleL, BCastleR);
        }
        else {
            return BoardStatus(!WhiteMove, false, WCastleL, WCastleR, false, false);
        }
    }

    //Moving a castling rook
    constexpr BoardStatus RookMove_Left() const {
        if (WhiteMove) {
            return BoardStatus(!WhiteMove, false, false, WCastleR, BCastleL, BCastleR);
        }
        else {
            return BoardStatus(!WhiteMove, false, WCastleL, WCastleR, false, BCastleR);
        }
    }

    constexpr BoardStatus RookMove_Right() const {
        if (WhiteMove) {
            return BoardStatus(!WhiteMove, false, WCastleL, false, BCastleL, BCastleR);
        }
        else {
            return BoardStatus(!WhiteMove, false, WCastleL, WCastleR, BCastleL, false);
        }
    }

    constexpr BoardStatus SilentMove() const {
        return BoardStatus(!WhiteMove, false, WCastleL, WCastleR, BCastleL, BCastleR);
    }
};

std::ostream& operator<<(std::ostream& os, const BoardStatus& dt);
std::ostream& operator<<(std::ostream& os, const BoardStatus& dt) {
    if (dt.WhiteMove) os << "w";
    else os << "b";

    if (dt.HasEPPawn) os << "ep:1";
    else os << "ep:0";

    if (!dt.WCastleL && !dt.WCastleR && !dt.BCastleL && !dt.BCastleR) 
    {
        os << " castle:0";
    }
    else {
        os << " castle:";
        if (dt.WCastleL) os << "Q";
        if (dt.WCastleR) os << "K";
        if (dt.BCastleL) os << "q";
        if (dt.BCastleR) os << "k";
    }
    return os;
}

struct FEN {
    static constexpr uint64_t FenToBmp(std::string_view FEN, char p)
    {
        uint64_t i = 0;
        char c{};
        int Field = 63;

        uint64_t result = 0;
        while ((c = FEN[i++]) != ' ')
        {
            uint64_t P = 1ull << Field;
            switch (c) {
                case '/': Field += 1; break;
                case '1': break;
                case '2': Field -= 1; break;
                case '3': Field -= 2; break;
                case '4': Field -= 3; break;
                case '5': Field -= 4; break;
                case '6': Field -= 5; break;
                case '7': Field -= 6; break;
                case '8': Field -= 7; break;
                default:
                    if (c == p) result |= P; //constexpr parsing happens here
            }
            Field--;
        }
        return result;        
    }
};

enum BoardPiece {
    Pawn, Knight, Bishop, Rook, Queen, King
};

struct Board {
    const map BPawn;
    const map Bknight;
    const map BBishop;
    const map BRook;
    const map BQueen;
    const map BKing;

    const map WPawn;
    const map Wknight;
    const map WBishop;
    const map WRook;
    const map WQueen;
    const map WKing;

    const map Black;
    const map White;
    const map Occ;

    constexpr Board(
        map bp, map bn, map bb, map br, map bq, map bk,
        map wp, map wn, map wb, map wr, map wq, map wk) :
        BPawn(bp), Bknight(bn), BBishop(bb), BRook(br), BQueen(bq), BKing(bk),
        WPawn(wp), Wknight(wn), WBishop(wb), WRook(wr), WQueen(wq), WKing(wk),
        Black(bp | bn | bb | br | bq | bk),
        White(wp | wn | wb | wr | wq | wk),
        Occ(Black | White)
    {

    }

    constexpr Board(std::string_view FEN) :
        Board(FEN::FenToBmp(FEN, 'p'), FEN::FenToBmp(FEN, 'n'), FEN::FenToBmp(FEN, 'b'), FEN::FenToBmp(FEN, 'r'), FEN::FenToBmp(FEN, 'q'), FEN::FenToBmp(FEN, 'k'),
            FEN::FenToBmp(FEN, 'P'), FEN::FenToBmp(FEN, 'N'), FEN::FenToBmp(FEN, 'B'), FEN::FenToBmp(FEN, 'R'), FEN::FenToBmp(FEN, 'Q'), FEN::FenToBmp(FEN, 'K'))
    {

    }

    template<BoardPiece piece, bool IsWhite>
    static constexpr Board MovePromote(const Board& existing, uint64_t from, uint64_t to)
    {
        const uint64_t rem = ~to;
        const map bp = existing.BPawn;
        const map bn = existing.Bknight;
        const map bb = existing.BBishop;
        const map br = existing.BRook;
        const map bq = existing.BQueen;
        const map bk  = existing.BKing;

        const map wp = existing.WPawn;
        const map wn = existing.Wknight;
        const map wb = existing.WBishop;
        const map wr = existing.WRook;
        const map wq = existing.WQueen;
        const map wk = existing.WKing;

        if constexpr (IsWhite) {
            if constexpr (BoardPiece::Queen == piece)   return Board(bp & rem, bn & rem, bb & rem, br & rem, bq & rem, bk, wp ^ from, wn, wb, wr, wq ^ to, wk);
            if constexpr (BoardPiece::Rook == piece)    return Board(bp & rem, bn & rem, bb & rem, br & rem, bq & rem, bk, wp ^ from, wn, wb, wr ^ to, wq, wk);
            if constexpr (BoardPiece::Bishop == piece)  return Board(bp & rem, bn & rem, bb & rem, br & rem, bq & rem, bk, wp ^ from, wn, wb ^ to, wr, wq, wk);
            if constexpr (BoardPiece::Knight == piece)  return Board(bp & rem, bn & rem, bb & rem, br & rem, bq & rem, bk, wp ^ from, wn ^ to, wb, wr, wq, wk);
        }
        else {
            if constexpr (BoardPiece::Queen == piece)   return Board(bp ^ from, bn, bb, br, bq ^ to, bk, wp & rem, wn & rem, wb & rem, wr & rem, wq & rem, wk);
            if constexpr (BoardPiece::Rook == piece)    return Board(bp ^ from, bn, bb, br ^ to, bq, bk, wp & rem, wn & rem, wb & rem, wr & rem, wq & rem, wk);
            if constexpr (BoardPiece::Bishop == piece)  return Board(bp ^ from, bn, bb ^ to, br, bq, bk, wp & rem, wn & rem, wb & rem, wr & rem, wq & rem, wk);
            if constexpr (BoardPiece::Knight == piece)  return Board(bp ^ from, bn ^ to, bb, br, bq, bk, wp & rem, wn & rem, wb & rem, wr & rem, wq & rem, wk);
        }
    }

    template<bool IsWhite>
    static constexpr Board MoveCastle(const Board& existing, uint64_t kingswitch, uint64_t rookswitch)
    {
        const map bp = existing.BPawn;
        const map bn = existing.Bknight;
        const map bb = existing.BBishop;
        const map br = existing.BRook;
        const map bq = existing.BQueen;
        const map bk  = existing.BKing;

        const map wp = existing.WPawn;
        const map wn = existing.Wknight;
        const map wb = existing.WBishop;
        const map wr = existing.WRook;
        const map wq = existing.WQueen;
        const map wk = existing.WKing;

        if constexpr (IsWhite) {
            return Board(bp, bn, bb, br, bq, bk, wp, wn, wb, wr ^ rookswitch, wq, wk ^ kingswitch);
        }
        else {
            return Board(bp, bn, bb, br ^ rookswitch, bq, bk ^ kingswitch, wp, wn, wb, wr, wq, wk);
        }
    }

    template<bool IsWhite>
    static constexpr Board MoveEP(const Board& existing, uint64_t from, uint64_t enemy, uint64_t to)
    {
        const uint64_t rem = ~enemy;
        const map bp = existing.BPawn;
        const map bn = existing.Bknight;
        const map bb = existing.BBishop;
        const map br = existing.BRook;
        const map bq = existing.BQueen;
        const map bk  = existing.BKing;

        const map wp = existing.WPawn;
        const map wn = existing.Wknight;
        const map wb = existing.WBishop;
        const map wr = existing.WRook;
        const map wq = existing.WQueen;
        const map wk = existing.WKing;
        const map mov = from | to;

        if constexpr (IsWhite) {
            return Board(bq & rem, bn & rem, bb & rem, br & rem, bq & rem, bk, wp ^ mov, wn, wb, wr, wq, wk);
        }
        else {
            return Board(bp ^ mov, bn, bb, br, bq, bk, wp & rem, wn & rem, wb & rem, wr & rem, wq & rem, wk);
        }
    }

    template<BoardPiece piece, bool IsWhite>
    static constexpr Board Move(const Board& existing, uint64_t from, uint64_t to, bool IsTaking)
    {
        if (IsTaking) return Move<piece, IsWhite, true>(existing, from, to);
        else return Move<piece, IsWhite, false>(existing, from, to);
    }

    template<BoardPiece piece, bool IsWhite, bool IsTaking>
    static constexpr Board Move(const Board& existing, uint64_t from, uint64_t to)
    {
        const map bp = existing.BPawn;
        const map bn = existing.Bknight;
        const map bb = existing.BBishop;
        const map br = existing.BRook;
        const map bq = existing.BQueen;
        const map bk  = existing.BKing;

        const map wp = existing.WPawn;
        const map wn = existing.Wknight;
        const map wb = existing.WBishop;
        const map wr = existing.WRook;
        const map wq = existing.WQueen;
        const map wk = existing.WKing;

        const map mov = from | to;

        if constexpr (IsTaking)
        {
            const uint64_t rem = ~to;
            if constexpr (IsWhite) {
                if (bk & mov == 0) throw std::runtime_error("Taking Black King is not legal!");
                if (to & existing.White == 0) throw std::runtime_error("Cannot move to square of same white color!");
                
                if constexpr (BoardPiece::Pawn == piece)    return Board(bp & rem, bn & rem, bb & rem, br & rem, bq & rem, bk, wp ^ mov, wn, wb, wr, wq, wk);
                if constexpr (BoardPiece::Knight == piece)  return Board(bp & rem, bn & rem, bb & rem, br & rem, bq & rem, bk, wp, wn ^ mov, wb, wr, wq, wk);
                if constexpr (BoardPiece::Bishop == piece)  return Board(bp & rem, bn & rem, bb & rem, br & rem, bq & rem, bk, wp, wn, wb ^ mov, wr, wq, wk);
                if constexpr (BoardPiece::Rook == piece)    return Board(bp & rem, bn & rem, bb & rem, br & rem, bq & rem, bk, wp, wn, wb, wr ^ mov, wq, wk);
                if constexpr (BoardPiece::Queen == piece)   return Board(bp & rem, bn & rem, bb & rem, br & rem, bq & rem, bk, wp, wn, wb, wr, wq ^ mov, wk);
                if constexpr (BoardPiece::King == piece)    return Board(bp & rem, bn & rem, bb & rem, br & rem, bq & rem, bk, wp, wn, wb, wr, wq, wk ^ mov);
            }
            else {
                if (wk & mov == 0) throw std::runtime_error("Taking White King is not legal!");
                if (to & existing.Black == 0) throw std::runtime_error("Cannot move to square of same black color!");

                if constexpr (BoardPiece::Pawn == piece)    return Board(bp ^ mov, bn, bb, br, bq, bk, wp & rem, wn & rem, wb & rem, wr & rem, wq & rem, wk);
                if constexpr (BoardPiece::Knight == piece)  return Board(bp, bn ^ mov, bb, br, bq, bk, wp & rem, wn & rem, wb & rem, wr & rem, wq & rem, wk);
                if constexpr (BoardPiece::Bishop == piece)  return Board(bp, bn, bb ^ mov, br, bq, bk, wp & rem, wn & rem, wb & rem, wr & rem, wq & rem, wk);
                if constexpr (BoardPiece::Rook == piece)    return Board(bp, bn, bb, br ^ mov, bq, bk, wp & rem, wn & rem, wb & rem, wr & rem, wq & rem, wk);
                if constexpr (BoardPiece::Queen == piece)   return Board(bp, bn, bb, br, bq ^ mov, bk, wp & rem, wn & rem, wb & rem, wr & rem, wq & rem, wk);
                if constexpr (BoardPiece::King == piece)    return Board(bp, bn, bb, br, bq, bk ^ mov, wp & rem, wn & rem, wb & rem, wr & rem, wq & rem, wk);
            }
        }
        else {
            if constexpr (IsWhite) {
                if (bk & mov == 0) throw std::runtime_error("Taking Black King is not legal!");
                if (to & existing.White == 0) throw std::runtime_error("Cannot move to square of same white color!");

                if constexpr (BoardPiece::Pawn == piece)    return Board(bp, bn, bb, br, bq, bk, wp ^ mov, wn, wb, wr, wq, wk);
                if constexpr (BoardPiece::Knight == piece)  return Board(bp, bn, bb, br, bq, bk, wp, wn ^ mov, wb, wr, wq, wk);
                if constexpr (BoardPiece::Bishop == piece)  return Board(bp, bn, bb, br, bq, bk, wp, wn, wb ^ mov, wr, wq, wk);
                if constexpr (BoardPiece::Rook == piece)    return Board(bp, bn, bb, br, bq, bk, wp, wn, wb, wr ^ mov, wq, wk);
                if constexpr (BoardPiece::Queen == piece)   return Board(bp, bn, bb, br, bq, bk, wp, wn, wb, wr, wq ^ mov, wk);
                if constexpr (BoardPiece::King == piece)    return Board(bp, bn, bb, br, bq, bk, wp, wn, wb, wr, wq, wk ^ mov);
            }
            else {
                if (wk & mov == 0) throw std::runtime_error("Taking White King is not legal!");
                if (to & existing.Black == 0) throw std::runtime_error("Cannot move to square of same black color!");

                if constexpr (BoardPiece::Pawn == piece)    return Board(bp ^ mov, bn, bb, br, bq, bk, wp, wn, wb, wr, wq, wk);
                if constexpr (BoardPiece::Knight == piece)  return Board(bp, bn ^ mov, bb, br, bq, bk, wp, wn, wb, wr, wq, wk);
                if constexpr (BoardPiece::Bishop == piece)  return Board(bp, bn, bb ^ mov, br, bq, bk, wp, wn, wb, wr, wq, wk);
                if constexpr (BoardPiece::Rook == piece)    return Board(bp, bn, bb, br ^ mov, bq, bk, wp, wn, wb, wr, wq, wk);
                if constexpr (BoardPiece::Queen == piece)   return Board(bp, bn, bb, br, bq ^ mov, bk, wp, wn, wb, wr, wq, wk);
                if constexpr (BoardPiece::King == piece)    return Board(bp, bn, bb, br, bq, bk ^ mov, wp, wn, wb, wr, wq, wk);
            }
        }
    }

    static constexpr Board Default() {
        return Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1");
    }
};