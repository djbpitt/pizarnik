<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:djb="http://www.obdurodon.org" xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs" version="2.0">
    <xsl:strip-space elements="table"/>
    <xsl:output method="xml" indent="no" doctype-system="about:legacy-compat"/>
    <xsl:function name="djb:titleCase" as="xs:string">
        <xsl:param name="input"/>
        <xsl:variable name="initial" select="substring($input, 1, 1)" as="xs:string"/>
        <xsl:variable name="remainder" select="substring($input, 2)" as="xs:string"/>
        <xsl:sequence select="concat(upper-case($initial), $remainder)"/>
    </xsl:function>
    <xsl:template match="/">
        <html>
            <head>
                <title>Pizarnik collation demo</title>
                <link rel="stylesheet" href="http://www.obdurodon.org/css/style.css" type="text/css"/>
                <style type="text/css">
                    table,
                    tr,
                    th,
                    td{
                        border: none;
                    }
                    th,
                    td{
                        text-align: left;
                        border-right: 1px solid gray;
                        border-left: 1px solid gray;
                    }
                    ins{
                        text-decoration: none;
                        color: green;
                    }
                    .add{
                        color: green;
                    }
                    .del,
                    .gap{
                        color: red;
                        text-decoration: line-through;
                    }
                    .label{
                        font-style: italic;
                    }</style>
            </head>
            <body>
                <h1>Pizarnik collation demo</h1>
                <xsl:apply-templates select="root/table"/>
            </body>
        </html>
    </xsl:template>
    <xsl:template match="table">
        <!-- collation sets -->
        <p class="label">
            <xsl:text>Line </xsl:text>
            <xsl:value-of select="position()"/>
        </p>
        <table>
            <xsl:apply-templates/>
        </table>
    </xsl:template>
    <xsl:template match="table/item">
        <!-- witness within a collation set -->
        <xsl:variable name="position" select="position()" as="xs:integer"/>
        <tr>
            <th>
                <xsl:value-of
                    select="djb:titleCase(../following-sibling::witnesses[1]/item[$position])"/>
            </th>
            <xsl:apply-templates/>
        </tr>
    </xsl:template>
    <xsl:template match="item/item">
        <!-- cells within a collation set -->
        <td>
            <xsl:apply-templates select="descendant::t"/>
        </td>
    </xsl:template>
    <xsl:template match="t">
        <xsl:apply-templates/>
        <xsl:text> </xsl:text>
    </xsl:template>
    <xsl:template match="add[@n = 'start']">
        <span class="add">
            <xsl:choose>
                <xsl:when test="@place eq 'margin'">
                    <xsl:text>\\</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text>\</xsl:text>
                </xsl:otherwise>
            </xsl:choose>
        </span>
    </xsl:template>
    <xsl:template match="add[@n = 'end']">
        <span class="add">
            <xsl:choose>
                <xsl:when test="preceding-sibling::add[1]/@place eq 'margin'">
                    <xsl:text>//</xsl:text>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:text>/</xsl:text>
                </xsl:otherwise>
            </xsl:choose>
        </span>
    </xsl:template>
    <xsl:template match="del[@n = 'start']">
        <span class="del">
            <xsl:text>(</xsl:text>
        </span>
    </xsl:template>
    <xsl:template match="del[@n = 'end']">
        <span class="del">
            <xsl:text>)</xsl:text>
        </span>
    </xsl:template>
    <xsl:template match="gap[@n = 'start']">
        <span class="gap">
            <xsl:for-each select="1 to @length">
                <xsl:text>.</xsl:text>
            </xsl:for-each>
        </span>
    </xsl:template>
    <xsl:template match="text()">
        <xsl:choose>
            <xsl:when
                test="preceding-sibling::node()[1][self::add] and following-sibling::node()[1][self::add]">
                <span class="add">
                    <xsl:value-of select="."/>
                </span>
            </xsl:when>
            <xsl:when
                test="preceding-sibling::node()[1][self::del or self::gap] and following-sibling::node()[1][self::del or self::gap]">
                <span class="del">
                    <xsl:value-of select="."/>
                </span>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="."/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
