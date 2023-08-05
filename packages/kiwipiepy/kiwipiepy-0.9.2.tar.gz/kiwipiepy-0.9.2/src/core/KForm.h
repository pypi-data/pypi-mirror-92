#pragma once

namespace kiwi
{
	enum class KPOSTag : uint8_t
	{
		UNKNOWN,
		NNG, NNP, NNB,
		VV, VA,
		MAG,
		NR, NP,
		VX,
		MM, MAJ,
		IC,
		XPN, XSN, XSV, XSA, XR,
		VCP, VCN,
		SF, SP, SS, SE, SO, SW,
		SL, SH, SN,
		W_URL, W_EMAIL, W_MENTION, W_HASHTAG,
		DEFAULT_TAG_SIZE,
		JKS = DEFAULT_TAG_SIZE, JKC, JKG, JKO, JKB, JKV, JKQ, JX, JC,
		EP, EF, EC, ETN, ETM,
		V,
		MAX,
	};

	enum class KCondVowel : uint8_t
	{
		none,
		any,
		vowel,
		vocalic,
		vocalicH,
		nonVowel,
		nonVocalic,
		nonVocalicH,
	};

	enum class KCondPolarity : char
	{
		none,
		positive,
		negative
	};

	inline bool isWebTag(KPOSTag t)
	{
		return KPOSTag::W_URL <= t && t <= KPOSTag::W_HASHTAG;
	}

	KPOSTag makePOSTag(const std::u16string& tagStr);
	const char* tagToString(KPOSTag t);
	const k_char* tagToStringW(KPOSTag t);
	struct KForm;

	struct KMorpheme
	{
#ifdef _DEBUG
		static size_t uid;
		size_t id;
#endif
		const k_string* kform = nullptr;
		KPOSTag tag = KPOSTag::UNKNOWN;
		KCondVowel vowel = KCondVowel::none;
		KCondPolarity polar = KCondPolarity::none;
		uint8_t combineSocket = 0;
		std::unique_ptr<std::vector<const KMorpheme*>> chunks;
		int32_t combined = 0;
		float userScore = 0;

		KMorpheme(const k_string& _form = {},
			KPOSTag _tag = KPOSTag::UNKNOWN,
			KCondVowel _vowel = KCondVowel::none,
			KCondPolarity _polar = KCondPolarity::none,
			uint8_t _combineSocket = 0)
			: tag(_tag), vowel(_vowel), polar(_polar), combineSocket(_combineSocket)
#ifdef  _DEBUG
			, id(uid++)
#endif //  _DEBUG
		{
		}

		KMorpheme(const KMorpheme& m) :
			kform(m.kform), tag(m.tag), vowel(m.vowel), polar(m.polar),
			combineSocket(m.combineSocket), chunks(m.chunks ? new std::vector<const KMorpheme*>(*m.chunks) : nullptr),
			combined(m.combined), userScore(m.userScore)
		{
		}

		const k_string& getForm() const { return *kform; }
		const KMorpheme* getCombined() const { return this + combined; }

		template<class _Istream>
		void readFromBin(_Istream& is, const std::function<const KMorpheme*(size_t)>& mapper);
		void writeToBin(std::ostream& os, const std::function<size_t(const KMorpheme*)>& mapper) const;

		std::ostream& print(std::ostream& os) const;
	};

	struct KForm
	{
		k_string form;
		KCondVowel vowel = KCondVowel::none;
		KCondPolarity polar = KCondPolarity::none;

		std::vector<const KMorpheme*> candidate;
		KForm(const k_char* _form = nullptr);
		KForm(const k_string& _form, KCondVowel _vowel, KCondPolarity _polar) 
			: form(_form), vowel(_vowel), polar(_polar)
		{}

		KForm(const KForm&) = default;
		KForm(KForm&&) = default;

		bool operator < (const KForm& o) const
		{
			if (form < o.form) return true;
			if (form > o.form) return false;
			if (vowel < o.vowel) return true;
			if (vowel > o.vowel) return false;
			return polar < o.polar;

		}

		KForm& operator=(const KForm&) = default;
		KForm& operator=(KForm&&) = default;

		template<class _Istream>
		void readFromBin(_Istream& is, const std::function<const KMorpheme*(size_t)>& mapper);
		void writeToBin(std::ostream& os, const std::function<size_t(const KMorpheme*)>& mapper) const;
	};

}
