bool separatePinyin(const std::string &pinyin, int tone, std::string &initial, std::string &final) {
    // special handing of pinyin conversion
    if (pinyin[0] == 'y')
    {
        final = pinyin;
        final[0] = 'i';
        // ya->ia, yan->ian, yang->iang, yao->iao, ye->ie, yo->io, yong->iong, you->iou
        // yi->i, yin->in, ying->ing
        // yu->v, yuan->van, yue->ve, yun->vn
        if (final.length() >= 2 && final[1] == 'u')
        {
            final[1] = L'v';
        }
        if (final.length()>= 2 && (final[1] == L'i' || final[1] == L'v'))
        {
            final= final.substr(1, pinyin.length()-1);
        }
        if (final == "io")
        {
            // final = "iou";
        }
        initial = "0";
    }
    else if (pinyin[0] == L'w')
    {
        // wa->ua, wo->uo, wai->uai, wei->uei, wan->uan, wen->uen, wang->uang, weng->ueng
        // wu->u
        // change 'w' to 'u', except 'wu->u'
        final = pinyin;
        final[0] = 'u';
        if (pinyin.length() >= 2 && pinyin[1] == L'u')
        {
            final = pinyin.substr(1, pinyin.length() - 1);
        }
        initial = "0";
    }
    else
    {
        // initial should not be empty
        std::string::size_type sf = pinyin.find_first_of("aeiouv");
        if (sf == std::string::npos)
        {
            return false;
        }
        initial = pinyin.substr(0, sf);
        final = pinyin.substr(sf, pinyin.length()-sf);

        bool retroflex = false;
        if (final[final.length()-1] == 'r')
        {
            retroflex = true;
            final = final.substr(0, final.length() - 1);
        }
        // special handling of final
        if (final == "i")
        {
            if (initial == "z" || initial == "c" || initial == "s")
            {
                // the final of "zi, ci, si" should be "-i"
                final = "ii";
            }
            else if (initial == "zh" || initial == "ch" || initial == "sh" || initial == "r")
            {
                // the final of "zhi, chi, shi, ri" should be "-I"
                final = "iii";
            }
        }
        else if (final[0] == L'u' && (initial == "j" ||  initial == "q" || initial == "x"))
        {
            // ju->jv, jue->jve, juan->jvan, jun->jvn,
            // qu->qv, que->qve, quan->qvan, qun->qvn,
            // xu->xv, xue->xve, xuan->xvan, xun->xvn
            // change all 'u' to 'v'
            final[0] = L'v';
        }
        else if (final == "ui")
        {
            // when there is initial
            // ui->uei
            final = "uei";
        }
        else if (final == "iu")
        {
            // when there is initial
            // iu->iou
            final = "iou";
        }
        else if (final == "un")
        {
            // when there is initial
            // un->uen
            final = "uen";
        }
        if (retroflex)
        {
            final += "r";
        }
        if (initial == "")
        {
            initial = "0";
        }
    }

    if (final.length() > 0 && final[final.length()-1] == 'r')
    {
        if (final == "er")
        {
            //printf (".%s.%s.%d.\n", initial.c_str(), final.c_str(), tone);
            if (initial == "0" && tone == 4)
            {
                final = "ar";
            }
        }
        else if (final == "iir" || final == "iiir" || final == "enr")
        {
            final = "eir";
        }
        else if (final == "air" || final == "anr")
        {
            final = "ar";
        }
        else if (final == "ianr")
        {
            final = "iar";
        }
        else if (final == "inr")
        {
            final = "ir";
        }
        else if (final == "uair" || final == "uanr")
        {
            final = "uar";
        }
        else if (final == "uenr")
        {
            final = "ueir";
        }
        else if (final == "vnr")
        {
            final = "vr";
        }
    }
    else if (initial == "0" && final == "o")
    {
        final = "ou";
    }
    return true;
}